import re
from .hook import Hook
from ..api import API


class UrlLabelHook(Hook):
    """
    Hook to label an issue based on the presence of a url.
    Args:
        url_pattern: string of the regular expression that the URL should match.
        new_labels: array of labels to apply if the url matches.
    """
    def __init__(self, url_pattern, labels):
        self.url_pattern = re.compile(url_pattern)
        self.new_labels = labels
        super(UrlLabelHook, self).__init__()

    def should_perform_action(self, payload, api=None):
        """
        Checks whether we need to apply a label to this issue.
        """
        try:
            text_source = payload.get("comment") or payload.get("issue")
            print self.url_pattern, text_source["body"]
            print self.url_pattern.search(text_source["body"])
            if self.url_pattern.search(text_source["body"]):
                return True
        except KeyError, err:
            print err

        return False

    def actions(self, payload, api):
        """
        List of actions.
        """
        return [
            {"action": api.add_labels,
             "args": {
                 "issue_url": payload["issue"]["url"],
                 "labels": self.new_labels
             },
            },
        ]
