from django.contrib.auth.models import User

from wsse.utils import get_secret, verify_wsse_digest


class WsseBackend(object):

    def authenticate(self, username, digest, nonce, timestamp):
        """Authenticate WSSE

        @type username: str
        @type digest: str
        @type nonce: str
        @type timestamp: str

        @rtype: User
            None if authentication fails
        """
        secret = get_secret(username)
        if secret is None:
            return None
        # TODO use the timestamp to handle stale requests
        if not verify_wsse_digest(secret, nonce, timestamp, digest):
            return None

        return User.objects.get(username__iexact=username)

    def get_user(self, user_id):
        """Retrieve the user's entry in the User model if it exists"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
