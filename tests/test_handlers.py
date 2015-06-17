from ghi_assist.webhook import Webhook

def test_handlers(capsys):
    """ Test adding handlers. """
    hook = Webhook()
    assert hook.handlers == {}, "No handlers."

    def pong_one():
        print "got ping"
    def pong_two():
        print "now pong"
    hook.register('ping', pong_one)
    hook.register('ping', pong_two)

    hook.respond_to('ping')
    out, _ = capsys.readouterr()
    assert out == "got ping\nnow pong\n", "Got ping handler responses."

def test_nonexistent_handler():
    """ Test trying to use an event we don't have handlers for. """
    hook = Webhook()
    hook.respond_to('unknown')
