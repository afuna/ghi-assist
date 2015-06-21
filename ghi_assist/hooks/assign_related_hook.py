import re
from .hook import Hook
from ..api import API

ISSUE_PATTERN = re.compile(r'#(\d+)')
ISSUE_URL_PATTERN = re.compile('{/number}')

class AssignRelatedHook(Hook):
    """
    Hook to assign an issue to the author of a pull request.
    """
    def __init__(self):
        self.related_issue_id = None
        self.related_issue_url = None
        self.related_issue = None
        super(AssignRelatedHook, self).__init__()

    def _related_issue_id(self, payload):
        """
        Looks for an issue id
        """
        match = ISSUE_PATTERN.search(payload["pull_request"]["title"]) or \
                ISSUE_PATTERN.search(payload["pull_request"]["body"])
        if match:
            return match.group(1)
        else:
            return None

    def should_perform_action(self, payload, api=None):
        """
        Checks whether we want to assign a related issue.
        """
        try:
            related_issue_id = self._related_issue_id(payload)
            if payload["action"] == "opened" and related_issue_id is not None:
                self.related_issue_id = int(related_issue_id)
                self.related_issue_url = ISSUE_URL_PATTERN.sub("/%s" % related_issue_id, \
                    payload["repository"]["issues_url"])

                # check if already assigned
                self.related_issue = api.issue(self.related_issue_url)
                if self.related_issue["assignee"] is not None:
                    return False

                return True
        except KeyError, err:
            print err

        return False

    def actions(self, payload, api=None):
        """
        List of actions.
        """
        return [
            {"action": api.assign_issue,
             "args": {
                 "issue_url": self.related_issue_url,
                 "assignee": payload["sender"]["login"]
             },
            },
            {"action": api.label_claimed,
             "args": {
                 "issue_url": self.related_issue_url,
                 "labels": self.related_issue["labels"]
             },
            },
        ]
