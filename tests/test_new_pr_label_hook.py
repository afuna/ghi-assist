from ghi_assist.hooks.new_pr_label_hook import NewPrLabelHook
from mock import Mock
import json

def test_no_labels():
    """Test no labels to apply."""
    hook = NewPrLabelHook()
    payload = {
        "action": "opened",
        "issue": {
            "labels": [],
        },
        "pull_request": {
            "body": "foo bar baz",
            "issue_url": "http://",
        }
    }
    assert hook.should_perform_action(payload), "No labels: mark as untriaged"
    assert hook.actions(payload, Mock())[0]["args"]["labels"] == ["status: untriaged"]

def test_labels_from_comments():
    """Test with new labels."""
    hook = NewPrLabelHook(whitelist=["foo"])
    payload = {
        "action": "opened",
        "issue": {
            "labels": [],
        },
        "pull_request": {
            "body": "##foo bar baz",
            "issue_url": "http://",
        }
    }
    assert hook.should_perform_action(payload), "Got labels."
    assert hook.actions(payload, Mock())[0]["args"]["labels"] == ["foo"]

def test_invalid_action():
    """Test with action other than "opened"."""
    hook = NewPrLabelHook()
    payload = {
        "action": "closed"
    }
    assert not hook.should_perform_action(payload), "Not newly opened."

def test_payload():
    """Test using "real" payload."""
    hook = NewPrLabelHook(whitelist=["foo"])
    payload = get_payload("new_pr_label.json")
    assert hook.should_perform_action(payload), "New PR with labels"
    assert hook.actions(payload, Mock())[0]["args"] == {
        "labels": ["foo"],
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/11",
    }

def get_payload(input_filename):
    """Parse the JSON payload and return an object."""
    with open("tests/payloads/" + input_filename) as input_file:
        return json.load(input_file)
