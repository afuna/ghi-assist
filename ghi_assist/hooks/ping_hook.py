from .hook import Hook

class PingHook(Hook):
    """
    Hook to respond to a ping.
    """

    def should_perform_action(self, payload, api=None):
        """
        Always respond to the ping.
        """
        return True

    def actions(self, payload, api):
        """
        List of actions.
        """
        return [{
            "action": lambda: "pong"
        }]
