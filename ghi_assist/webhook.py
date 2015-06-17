"""
Webhook for Github events.
"""
import hmac
from hashlib import sha1

class Webhook(object):
    def __init__(self, secret=None):
        self.handlers = {}
        self.secret = secret

    def signature_valid(self, data=None, signed_data=None, digest=sha1):
        """
        Checks if the signature from github matches the expected.

        Args:
            data: string of request data
            signed_data: signature provided by github
            digest: digest module to use (only sha1 is supported currently)
        Returns:
            True if our calculated signature matches the signature provided by Github.
            False otherwise.
        """
        mac = hmac.new(self.secret, msg=data, digestmod=digest)
        return hmac.compare_digest(mac.hexdigest(), signed_data)

    def register(self, event, handler):
        """
        Register a handler for an event.

        Args:
            event: string of event type from https://developer.github.com/v3/activity/events/types/.
        """
        handlers = self.handlers.setdefault(event, [])
        handlers.append(handler)

    def respond_to(self, event):
        """
        Run all handlers for an event.

        Args:
            event: string of event type from https://developer.github.com/v3/activity/events/types/.
        """

        if event not in self.handlers:
            return

        for func in self.handlers[event]:
            func()
