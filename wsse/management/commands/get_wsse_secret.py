from django.core.management.base import BaseCommand
from wsse.utils import get_secret


class Command(BaseCommand):
    help = 'Get the WSSE token for the specified users.'

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='+', type=str)

    def handle(self, *args, **options):
        for username in options['usernames']:
            self.stdout.write('{username}: {token}\n'.format(
                username=username, token=get_secret(username)))
