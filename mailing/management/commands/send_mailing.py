from django.core.management import BaseCommand
from mailing.services import send_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mailing()
