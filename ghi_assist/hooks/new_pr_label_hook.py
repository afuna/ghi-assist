from .hook import Hook
from ..api import API
from ..utils import extract_labels

class NewPrLabelHook(Hook):
    """Hook to label a pull request based on its text."""
    def __init__(self, payload, whitelist=None, aliases=None):
        self.labels = None
        self.whitelist = whitelist
        self.aliases = aliases
        super(NewPrLabelHook, self).__init__(payload)

    def should_perform_action(self):
        """
        True if we detected labels.
        """
        try:
            payload = self.payload
            if payload["action"] != "opened":
                return False

            labels = extract_labels(payload["pull_request"]["body"],
                                    whitelist=self.whitelist,
                                    aliases=self.aliases)
            if len(labels) == 0:
                labels.append("status: untriaged")

            if len(labels) > 0:
                self.labels = labels
                return True
        except KeyError, err:
            print err

        return False

    def actions(self):
        """
        List of actions.
        """
        api = API()
        return [
            {"action": api.replace_labels,
             "args": {
                 "labels": self.labels,
                 "issue_url": self.payload["pull_request"]["issue_url"],
             },
            }
        ]
