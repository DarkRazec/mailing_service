from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='content_manager')
        if created:
            [
                group.permissions.add(permission) for permission in
                Permission.objects.filter(content_type=ContentType.objects.get_for_model(Post)) if
                permission != 'add_post'
            ]
            group.save()
            print('Группа создана')
        else:
            print('Группа уже существует')
