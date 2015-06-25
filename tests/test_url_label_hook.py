from ghi_assist.hooks.url_label_hook import UrlLabelHook
from mock import Mock
import json

support_url_regex = r"https?://www\.dreamwidth\.org/support/see_request\?id=\d+"

def test_no_url():
    """Test a comment with no urls."""
    hook = UrlLabelHook(support_url_regex, ["from: support"])
    payload = {
        "comment": {
            "body": "Some comment here. Nothing special."
        }
    }
    assert not hook.should_perform_action(payload), "No-op"

def test_http_url():
    """Test http url."""
    hook = UrlLabelHook(support_url_regex, ["from: support"])
    payload = {
        "comment": {
            "body": "This was reported! http://www.dreamwidth.org/support/see_request?id=12345"
        }
    }
    assert hook.should_perform_action(payload), "Has http url"

def test_https_url():
    """Test https url."""
    hook = UrlLabelHook(support_url_regex, ["from: support"])
    payload = {
        "comment": {
            "body": "This was reported! https://www.dreamwidth.org/support/see_request?id=12345"
        }
    }
    assert hook.should_perform_action(payload), "Has https url"


def test_new_issue():
    """Test new issue (instead of comment)."""
    hook = UrlLabelHook(support_url_regex, ["from: support"])
    payload = {
        "issue": {
            "body": "This was reported! http://www.dreamwidth.org/support/see_request?id=12345"
        }
    }
    assert hook.should_perform_action(payload), "Has url"


def test_payload_new_issue():
    """Test adding label using a JSON payload when opening a new issue. Just a double-check."""
    hook = UrlLabelHook(support_url_regex, ["from: support"])
    payload = get_payload('url_label_new_issue.json')
    assert hook.should_perform_action(payload), "Found url."

    actions = hook.actions(payload, Mock())
    assert actions[0]["args"] == {
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/10",
        "labels": ["from: support"]
    }

def test_payload_comment():
    """Test adding label using a JSON payload when commenting. Just a double-check."""
    hook = UrlLabelHook(support_url_regex, ["from: support"])
    payload = get_payload('url_label_comment.json')
    assert hook.should_perform_action(payload), "Found url."

    actions = hook.actions(payload, Mock())
    assert actions[0]["args"] == {
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/14",
        "labels": ["from: support"]
    }


def get_payload(input_filename):
    """Parse the JSON payload and return an object."""
    with open("tests/payloads/" + input_filename) as input_file:
        return json.load(input_file)

