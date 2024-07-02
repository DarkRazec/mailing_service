from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from mailing.models import Mailing, Message, Client
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='mailing_moderator')
        if created:
            content_type = ContentType.objects.get_for_model(Mailing)
            group.permissions.add(Permission.objects.get(codename='view_mailing', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='is_active', content_type=content_type))
            content_type = ContentType.objects.get_for_model(Message)
            group.permissions.add(Permission.objects.get(codename='view_message', content_type=content_type))
            content_type = ContentType.objects.get_for_model(Client)
            group.permissions.add(Permission.objects.get(codename='view_client', content_type=content_type))
            content_type = ContentType.objects.get_for_model(User)
            group.permissions.add(Permission.objects.get(codename='is_active', content_type=content_type))
            group.save()
            print('Группа создана')
        else:
            print('Группа уже существует')
