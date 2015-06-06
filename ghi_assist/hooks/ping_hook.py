from .hook import Hook

class PingHook(Hook):
    """
    Hook to respond to a ping.
    """

    def should_perform_action(self):
        """
        Always respond to the ping.
        """
        return True

    def actions(self):
        """
        List of actions.
        """
        return []
