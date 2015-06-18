import re
from .hook import Hook
from ..api import API

# match "claim", "claimed", "claiming"
CLAIM_PATTERN = re.compile(r'\bclaim(?:ed|ing)?\b', re.I)

class ClaimHook(Hook):
    """
    Hook to claim an issue based on comment text.
    """
    def _claimed(self, payload):
        """
        Checks whether the comment content tries to "claim" the issue.
        """
        return CLAIM_PATTERN.search(payload["comment"]["body"])

    def should_perform_action(self, payload, api=None):
        """
        Checks whether we should claim this issue.
        """
        try:
            if payload["issue"]["assignee"] is None and self._claimed(payload):
                return True
        except KeyError, err:
            print err

        return False

    def actions(self, payload, api):
        """
        List of actions.
        """
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
