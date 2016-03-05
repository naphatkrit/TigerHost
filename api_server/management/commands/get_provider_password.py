from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Get the password to the specified provider for the specified user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('provider', type=str)

    def handle(self, *args, **options):
        user = User.objects.get(username=options['username'])
        provider = options['provider']
        c = user.profile.get_credential(provider)
        self.stdout.write('{}\n'.format(c.get_password()))
