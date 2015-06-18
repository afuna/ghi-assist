from bottle import request, post, run, abort, Bottle
import json
from os.path import normpath, dirname, abspath, join
from ghi_assist.utils import byteify
from ghi_assist.webhook import Webhook
from ghi_assist.hooks import AssignRelatedHook, ClaimHook, CommentLabelHook, NewIssueLabelHook, \
    NewPrLabelHook, PingHook

app = Bottle()
path = normpath(abspath(dirname(__file__)))
with open(join(path, 'config.json')) as config_file:
    app.config.load_dict(byteify(json.load(config_file)))

webhook = Webhook(secret=app.config["github.secret"], api_token=app.config["github.api_token"])
webhook.register("ping", PingHook())
webhook.register("issue_comment", CommentLabelHook(
    whitelist=app.config["labels.whitelist"],
    aliases=app.config["labels.aliases"]
))
webhook.register("issue_comment", ClaimHook())
webhook.register("issues", NewIssueLabelHook(
    whitelist=app.config["labels.whitelist"],
    aliases=app.config["labels.aliases"]
))
webhook.register("pull_request", NewPrLabelHook(
    whitelist=app.config["labels.whitelist"],
    aliases=app.config["labels.aliases"]
))
webhook.register("pull_request", AssignRelatedHook())

@post('/')
def github_webhook():
    """
    Main app entrypoint.
    """
    signature_header = request.headers.get('X-Hub-Signature')
    if signature_header is None:
        abort(403, "No X-Hub-Signature header.")

    digest_mode, signature = signature_header.split('=')
    if digest_mode != "sha1":
        abort(501, "'%s' not supported." % digest_mode)
    if not webhook.signature_valid(data=request.body.read(), signed_data=signature):
        abort(403, "Signature does not match expected value.")

    event = request.headers.get('X-GitHub-Event')
    responses = webhook.respond_to(event, request.json)
    return "Responded to %s.\n%s" % (event, "\n".join(responses))

run(host='localhost', port=8080)