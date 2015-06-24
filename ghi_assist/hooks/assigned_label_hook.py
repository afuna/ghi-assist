from .hook import Hook
from ..utils import filter_by_claimed


class AssignedLabelHook(Hook):
    """
    Hook to add or remove a the claimed label after (un)assignmhent.
    """

    def __init__(self):
        self.labels = None
        super(AssignedLabelHook, self).__init__()

    def should_perform_action(self, payload, api=None):
        """
        Check whether we need to add or remove the label.
        """
        try:
            action = payload["action"]
            labels = payload["issue"]["labels"]
        except KeyError, err:
            print err
            return False

        if action == "assigned":
            self.labels, updated_status = filter_by_claimed(labels, True)
        elif action == "unassigned":
            self.labels, updated_status = filter_by_claimed(labels, False)
        else:
            updated_status = False

        return updated_status

    def actions(self, payload, api):
        """
        Return the singleton list of actions to perform.

        There is only one action necessary here: replace the old labels with
        the new ones.
        """
        return [{"action": api.replace_labels,
                 "args": {"labels": self.labels,
                          "issue_url": payload["issue"]["url"]}}]
