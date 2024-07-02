import json

from django.core.management import BaseCommand

from mailing.models import Mailing, Message, Client
from users.models import User


class Command(BaseCommand):

    @staticmethod
    def json_read_mailings():
        # Получаем данные из фикстур с категориями
        with open('data/mailings_data.json', encoding='utf-16') as f:
            return json.load(f)

    @staticmethod
    def json_read_messages():
        # Получаем данные из фикстур с продуктами
        with open('data/messages_data.json', encoding='utf-16') as f:
            return json.load(f)

    @staticmethod
    def json_read_clients():
        # Получаем данные из фикстур с продуктами
        with open('data/clients_data.json', encoding='utf-16') as f:
            return json.load(f)

    def handle(self, *args, **options):
        Mailing.objects.all().delete()
        Message.objects.all().delete()
        Client.objects.all().delete()

        # Списки для хранения объектов
        messages_for_create = [Message(
            id=message['pk'],
            title=message['fields']['title'],
            body=message['fields']['body'],
            user=User.objects.get(pk=message['fields']['user']),
        ) for message in Command.json_read_messages()]

        Message.objects.bulk_create(messages_for_create)

        clients_for_create = [Client(
            id=client['pk'],
            **client['fields']
        ) for client in Command.json_read_clients()]

        Client.objects.bulk_create(clients_for_create)

        mailings_for_create = [Mailing(
            id=mailing['pk'],
            date_time=mailing['fields']['date_time'],
            end_date_time=mailing['fields']['end_date_time'],
            status=mailing['fields']['status'],
            is_active=mailing['fields']['is_active'],
            message=Message.objects.get(pk=mailing['fields']['message']),
            user=User.objects.get(pk=mailing['fields']['user']),
        ) for mailing in Command.json_read_mailings()]

        # Создаем объекты в базе с помощью метода bulk_create()
        Mailing.objects.bulk_create(mailings_for_create)

        for mailing in Command.json_read_mailings():
            mailing_instance = Mailing.objects.get(pk=mailing['pk'])
            client_ids = mailing['fields']['clients']
            clients = Client.objects.filter(pk__in=client_ids)
            mailing_instance.clients.set(clients)
