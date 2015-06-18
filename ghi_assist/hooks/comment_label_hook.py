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

    def should_perform_action(self, payload):
        """
        True if we detected labels.
        """
        try:
            labels = extract_labels(payload["comment"]["body"],
                                    whitelist=self.whitelist, aliases=self.aliases)

            force_replace, updated_status = False, False
            if len(labels) > 0:
                force_replace = True

            # update claimed status only if comment is to an issue (not PR)
            if "pull_request" not in payload["issue"]:
                if len(labels) == 0:
                    labels = payload["issue"]["labels"]
                else:
                    labels = [{"name": label} for label in labels]

                labels, updated_status = filter_by_claimed(
                    labels,
                    claimed=payload["issue"]["assignee"] is not None
                )

            if len(labels) > 0 and (force_replace or updated_status):
                self.labels = labels
                return True
        except KeyError, err:
            print err

        return False

    def actions(self, payload):
        """
        List of actions.
        """
        api = API()
        return [
            {"action": api.replace_labels,
             "args": {
                 "labels": self.labels,
                 "issue_url": payload["issue"]["url"],
             },
            }
        ]
