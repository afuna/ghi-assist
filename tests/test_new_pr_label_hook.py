from ghi_assist.hooks.new_pr_label_hook import NewPrLabelHook
import json

def test_no_labels():
    """Test no labels to apply."""
    hook = NewPrLabelHook({
        "action": "opened",
        "issue": {
            "assignee": None,
            "labels": [],
        },
        "pull_request": {
            "body": "foo bar baz",
            "issue_url": "http://",
        }
    })
    assert hook.should_perform_action(), "No labels: mark as untriaged"
    assert hook.actions()[0]["args"]["labels"] == ["status: untriaged"]

def test_labels_assigned():
    """Test with new labels."""
    hook = NewPrLabelHook({
        "action": "opened",
        "issue": {
            "assignee": {},
            "labels": [],
        },
        "pull_request": {
            "body": "##foo bar baz",
            "issue_url": "http://",
        }
    }, whitelist=["foo"])
    assert hook.should_perform_action(), "Got labels."
    assert hook.actions()[0]["args"]["labels"] == ["foo"]

def test_labels_unassigned():
    """Test with new labels."""
    hook = NewPrLabelHook({
        "action": "opened",
        "issue": {
            "assignee": None,
            "labels": [],
        },
        "pull_request": {
            "body": "##foo bar baz",
            "issue_url": "http://",
        }
    }, whitelist=["foo"])
    assert hook.should_perform_action(), "Got labels."
    assert hook.actions()[0]["args"]["labels"] == ["foo"]

def test_invalid_action():
    """Test with action other than "opened"."""
    hook = NewPrLabelHook({
        "action": "closed"
    })
    assert not hook.should_perform_action(), "Not newly opened."

def test_payload():
    """Test using "real" payload."""
    hook = NewPrLabelHook(get_payload("new_pr_label.json"), whitelist=["foo"])
    assert hook.should_perform_action(), "New PR with labels"
    assert hook.actions()[0]["args"] == {
        "labels": ["foo"],
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/11",
    }

def get_payload(input_filename):
    """Parse the JSON payload and return an object."""
    with open("tests/payloads/" + input_filename) as input_file:
        return json.load(input_file)
