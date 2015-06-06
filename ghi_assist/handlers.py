"""
Webhook for Github events.
"""
class Webhook(object):
    def __init__(self):
        self.handlers = {}

    def register(self, event, handler):
        """
        Register a handler for an event.

        Args:
            event: string of event type from https://developer.github.com/v3/activity/events/types/.
        """
        handlers = self.handlers.setdefault(event, [])
        handlers.append(handler)

    def respond_to(self, event):
        """
        Run all handlers for an event.

        Args:
            event: string of event type from https://developer.github.com/v3/activity/events/types/.
        """

        if event not in self.handlers:
            return

        for func in self.handlers[event]:
            func()
