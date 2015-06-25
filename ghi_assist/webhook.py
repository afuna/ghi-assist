"""
Webhook for Github events.
"""
import hmac
from hashlib import sha1
from ghi_assist.api import API

class Webhook(object):
    def __init__(self, secret=None, api_token=None):
        self.handlers = {}
        self.secret = secret
        self.api = API(api_token)

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
        try:
            return hmac.compare_digest(mac.hexdigest(), signed_data)
        except AttributeError:
            # may leak information, but compare_digest does not exist in Python < 2.7.7
            return mac.hexdigest() == signed_data

    def register(self, event, handler):
        """
        Register a handler for an event.

        Args:
            event: string of event type from https://developer.github.com/v3/activity/events/types/.
        """
        handlers = self.handlers.setdefault(event, [])
        handlers.append(handler)

    def respond_to(self, event, payload):
        """
        Run all handlers for an event.

        Args:
            event: string of event type from https://developer.github.com/v3/activity/events/types/.
        """

        if event not in self.handlers:
            return []

        responses = []
        for hook in self.handlers[event]:
            if hook.should_perform_action(payload, self.api):
                for action in hook.actions(payload, self.api):
                    args = action.get("args") or {}
                    response = action["action"](**args)
                    if response is not None:
                        responses.append(response)
        return responses

    def load_repo_labels(self, repository):
        """
        Load a list of labels from a repository.

        Args:
            repository: repository name (e.g., "organization/repository").
        Returns:
            A list of labels.
        """
        labels = self.api.get_repo_labels("https://api.github.com/repos/%s/labels" % repository)
        return [l["name"] for l in labels]