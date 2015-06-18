from ghi_assist.hooks.comment_label_hook import CommentLabelHook
import json

def test_no_labels():
    """Test no labels to apply."""
    hook = CommentLabelHook()
    payload = {
        "comment": {
            "body": "foo bar baz"
        },
        "issue": {
            "assignee": {},
            "url": "http://",
        },
    }
    assert not hook.should_perform_action(payload), "No labels"

def test_labels_assigned():
    """Test with new labels."""
    hook = CommentLabelHook(whitelist=["foo"])
    payload = {
        "comment": {
            "body": "##foo bar baz"
        },
        "issue": {
            "assignee": {},
            "url": "http://",
        },
    }
    assert hook.should_perform_action(payload), "Got labels."
    assert hook.actions(payload)[0]["args"]["labels"] == ["foo", "status: claimed"]

def test_labels_unassigned():
    """Test with new labels."""
    hook = CommentLabelHook(whitelist=["foo"])
    payload = {
        "comment": {
            "body": "##foo bar baz"
        },
        "issue": {
            "assignee": None,
            "url": "http://",
        },
    }
    assert hook.should_perform_action(payload), "Got labels."
    assert hook.actions(payload)[0]["args"]["labels"] == ["foo"]

def test_existing_labels():
    """Test with existing labels."""
    hook = CommentLabelHook(whitelist=["foo"])
    payload = {
        "comment": {
            "body": "##foo bar baz"
        },
        "issue": {
            "assignee": {},
            "labels": [{"name": "existing"}],
            "url": "http://",
        },
    }
    assert hook.should_perform_action(payload), "Got labels."
    assert hook.actions(payload)[0]["args"]["labels"] == ["foo", "status: claimed"]

def test_labels_pr():
    """Test with labels, but for a pull request."""
    hook = CommentLabelHook(whitelist=["foo"])
    payload = {
        "comment": {
            "body": "##foo bar baz"
        },
        "issue": {
            "assignee": {},
            "pull_request": {},
            "url": "http://",
        },
    }
    assert hook.should_perform_action(payload), "Got labels."
    assert hook.actions(payload)[0]["args"]["labels"] == ["foo"]

def test_payload():
    """Test using a 'real' payload."""
    hook = CommentLabelHook(
        whitelist=["foo"]
    )
    payload = get_payload('issue_comment_label.json')
    assert hook.should_perform_action(payload), "Issue comment with labels."

    actions = hook.actions(payload)
    assert actions[0]["args"] == {
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/14",
        "labels": ["foo", "status: claimed"]
    }

def get_payload(input_filename):
    """Parse the JSON payload and return an object."""
    with open("tests/payloads/" + input_filename) as input_file:
        return json.load(input_file)
