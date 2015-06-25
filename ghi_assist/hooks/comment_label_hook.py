from .hook import Hook
from ..api import API
from ..utils import extract_labels, filter_by_claimed

class CommentLabelHook(Hook):
    """
    Hook to label an issue based on text from a new comment.
    """
    def __init__(self, whitelist=None, aliases=None):
        self.labels = None
        self.whitelist = whitelist
        self.aliases = aliases
        super(CommentLabelHook, self).__init__()

    def should_perform_action(self, payload, api=None):
        """
        True if we detected labels.
        """
        try:
            labels = extract_labels(payload["comment"]["body"],
                                    whitelist=self.whitelist, aliases=self.aliases)
            if len(labels) > 0:
                self.labels = labels
                return True
        except KeyError, err:
            print err

        return False

    def actions(self, payload, api):
        """
        List of actions.
        """
        return [
            {"action": api.replace_labels,
             "args": {
                 "labels": self.labels,
                 "issue_url": payload["issue"]["url"],
             },
            }
        ]
