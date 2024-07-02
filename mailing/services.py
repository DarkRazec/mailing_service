import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.mail import send_mail
from django.db.models import Count

from mailing.models import Mailing, AttemptLogs, Client


def send_mailing() -> None:
    """
    Отправляет письма на указанный почтовый ящик и создает лог отправки
    """
    current_datetime = datetime.now(pytz.timezone(settings.TIME_ZONE))
    mailings = Mailing.objects.filter(date_time__lte=current_datetime, is_active=True,
                                      status__in=[Mailing.STARTED, Mailing.NEW])
    print(f'Количество рассылок для отправки: {mailings.count()}')

    for mailing in mailings:
        status = False
        response = ''
        print(f'Рассылка ID: {mailing.id}')
        clients = mailing.clients.all()
        try:
            server_response = send_mail(
                subject=mailing.message.title,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.mail for client in clients],
                fail_silently=False,
            )
            status = True
            response = server_response
            match mailing.frequency:
                case Mailing.ONCE:
                    mailing.status = Mailing.COMPLETED
                case Mailing.DAILY:
                    mailing.status = Mailing.STARTED
                    mailing.date_time += timedelta(days=1)
                case Mailing.WEEKLY:
                    mailing.status = Mailing.STARTED
                    mailing.date_time += timedelta(weeks=1)

        except smtplib.SMTPException as e:
            response = str(e)

        finally:
            (AttemptLogs.objects.create(
                date_time=mailing.date_time,
                status=status,
                response=response,
                mailing=mailing,
            )).save()

        if mailing.status == Mailing.STARTED and mailing.date_time < mailing.end_date_time:
            print(f'Обновленное время для рассылки ID {mailing.id}: {mailing.date_time}')

        else:
            mailing.status = Mailing.COMPLETED

        mailing.save()


def start_scheduler() -> None:
    """
    Запускает планировщик задач
    """
    print('Планировщик задач запускается...')
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)

    if not scheduler.running:
        scheduler.start()

    print('Планировщик задач запущен')


def clear_cache(cache_prefix: str, object_id: set) -> None:
    """
    Удаляет записи в кэше по object_id
    :param cache_prefix: Префикс для поиска по кэшу. В данном случае, скорее, по имени, с которым кэш был записан
    :param object_id: ID объекта, который был записан в кэш
    """
    cache.delete(make_template_fragment_key(cache_prefix, object_id))
    cache.delete(make_template_fragment_key(cache_prefix + 's', object_id))


def count_unique_clients() -> int:
    """Возвращает количество уникальных клиентов среди всех рассылок"""
    clients = Client.objects.annotate(num_mailings=Count('mailing'))
    return clients.filter(num_mailings=1).count()
