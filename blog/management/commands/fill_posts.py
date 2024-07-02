import json

from django.core.management import BaseCommand

from blog.models import Post
from mailing.models import Mailing, Message, Client
from users.models import User


class Command(BaseCommand):

    @staticmethod
    def json_read_posts():
        # Получаем данные из фикстур с категориями
        with open('data/posts_data.json', encoding='utf-16') as f:
            return json.load(f)

    def handle(self, *args, **options):
        Post.objects.all().delete()

        posts_for_create = [Post(
            id=post['pk'],
            name=post['fields']['name'],
            desc=post['fields']['desc'],
            image=post['fields']['image'],
            user=User.objects.get(pk=post['fields']['user']),
            is_published=post['fields']['is_published'],
        ) for post in Command.json_read_posts()]

        # Создаем объекты в базе с помощью метода bulk_create()
        Post.objects.bulk_create(posts_for_create)
