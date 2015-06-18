from ghi_assist.webhook import Webhook
from ghi_assist.hooks.hook import Hook

def print_message(message=""):
    print message

class PongOne(Hook):
    def should_perform_action(self, payload, api=None):
        return True

    def actions(self, payload, api):
        return [{
            "action": print_message,
            "args": {
                "message": "got ping"
            }
        }]

class PongTwo(Hook):
    def should_perform_action(self, payload, api=None):
        return True

    def actions(self, payload, api):
        return [{
            "action": print_message,
            "args": {
                "message": "now pong"
            }
        }]

def test_handlers(capsys):
    """ Test adding handlers. """
    hook = Webhook()
    assert hook.handlers == {}, "No handlers."

    hook.register("ping", PongOne())
    hook.register("ping", PongTwo())
    hook.respond_to('ping', {})
    out, _ = capsys.readouterr()
    assert out == "got ping\nnow pong\n", "Got ping handler responses."

def test_nonexistent_handler():
    """ Test trying to use an event we don't have handlers for. """
    hook = Webhook()
    hook.respond_to('unknown', {})
