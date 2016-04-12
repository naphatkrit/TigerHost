from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Get the password to the specified backend for the specified user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('backend', type=str)

    def handle(self, *args, **options):
        """Lookup the user using the username and backend, then write the PaaS password to stdout"""
        user = User.objects.get(username=options['username'])
        backend = options['backend']
        c = user.profile.get_credential(backend)
        self.stdout.write('{}\n'.format(c.get_password()))
