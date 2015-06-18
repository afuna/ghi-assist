class Hook(object):
    """
    Base hook class. Should be subclassed to be used.

    Subclasses must implement should_perform_action and perform_action.
    """
    def should_perform_action(self, payload, api=None):
        """
        Checks the payload to determine if we should perform the action or not.

        Returns:
            True / False.
        """
        raise NotImplementedError

    def actions(self, payload, api):
        """
        A list of actions that we want to perform for this hook.

        Args:
            None
        Returns:
            An array of actions in the form of:

            {
                "action": function_name,
                "args": { key1: value1, key2... }
            }
        """
        raise NotImplementedError
