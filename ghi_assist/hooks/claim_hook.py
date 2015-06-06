import re
from .hook import Hook
from ..api import API

# match "claim", "claimed", "claiming"
CLAIM_PATTERN = re.compile(r'\bclaim(?:ed|ing)?\b', re.I)

class ClaimHook(Hook):
    """
    Hook to claim an issue based on comment text.
    """
    def _claimed(self):
        """
        Checks whether the comment content tries to "claim" the issue.
        """
        return CLAIM_PATTERN.search(self.payload["comment"]["body"])

    def should_perform_action(self):
        """
        Checks whether we should claim this issue.
        """
        try:
            if self.payload["issue"]["assignee"] is None and self._claimed():
                return True
        except KeyError:
            pass

        return False

    def actions(self):
        """
        List of actions.
        """
        payload = self.payload
        api = API()
        return [
            {"action": api.assign_issue,
             "args": {
                 "issue_url": payload["issue"]["url"],
                 "assignee": payload["comment"]["user"]["login"]
             },
            },
            {"action": api.label_claimed,
             "args": {
                 "issue_url": payload["issue"]["url"],
                 "labels": payload["issue"]["labels"]
             },
            },
        ]
