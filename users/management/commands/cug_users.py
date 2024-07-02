from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from blog.models import Post
from mailing.models import Mailing, Message, Client


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='users')
        if created:
            content_type = ContentType.objects.get_for_model(Mailing)
            group.permissions.add(Permission.objects.get(codename='add_mailing', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='view_mailing', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='change_mailing', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='delete_mailing', content_type=content_type))
            content_type = ContentType.objects.get_for_model(Message)
            group.permissions.add(Permission.objects.get(codename='add_message', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='view_message', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='change_message', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='delete_message', content_type=content_type))
            content_type = ContentType.objects.get_for_model(Client)
            group.permissions.add(Permission.objects.get(codename='add_client', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='view_client', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='change_client', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='delete_client', content_type=content_type))
            content_type = ContentType.objects.get_for_model(Post)
            group.permissions.add(Permission.objects.get(codename='add_post', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='view_post', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='change_post', content_type=content_type))
            group.permissions.add(Permission.objects.get(codename='delete_post', content_type=content_type))
            group.save()
            print('Группа создана')
        else:
            print('Группа уже существует')
