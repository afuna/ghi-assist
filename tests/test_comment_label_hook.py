from ghi_assist.hooks.comment_label_hook import CommentLabelHook
import json

def test_no_labels():
    """Test no labels to apply."""
    hook = CommentLabelHook({
        "comment": {
            "body": "foo bar baz"
        },
        "issue": {
            "assignee": {},
            "url": "http://",
        },
    })
    assert not hook.should_perform_action(), "No labels"

def test_labels_assigned():
    """Test with new labels."""
    hook = CommentLabelHook({
        "comment": {
            "body": "##foo bar baz"
        },
        "issue": {
            "assignee": {},
            "url": "http://",
        },
    }, whitelist=["foo"])
    assert hook.should_perform_action(), "Got labels."
    assert hook.actions()[0]["args"]["labels"] == ["foo", "status: claimed"]

def test_labels_unassigned():
    """Test with new labels."""
    hook = CommentLabelHook({
        "comment": {
            "body": "##foo bar baz"
        },
        "issue": {
            "assignee": None,
            "url": "http://",
        },
    }, whitelist=["foo"])
    assert hook.should_perform_action(), "Got labels."
    assert hook.actions()[0]["args"]["labels"] == ["foo"]

def test_existing_labels():
    """Test with existing labels."""
    hook = CommentLabelHook({
        "comment": {
            "body": "##foo bar baz"
        },
        "issue": {
            "assignee": {},
            "labels": [{"name": "existing"}],
            "url": "http://",
        },
    }, whitelist=["foo"])
    assert hook.should_perform_action(), "Got labels."
    assert hook.actions()[0]["args"]["labels"] == ["foo", "status: claimed"]

def test_labels_pr():
    """Test with labels, but for a pull request."""
    hook = CommentLabelHook({
        "comment": {
            "body": "##foo bar baz"
        },
        "issue": {
            "assignee": {},
            "pull_request": {},
            "url": "http://",
        },
    }, whitelist=["foo"])
    assert hook.should_perform_action(), "Got labels."
    assert hook.actions()[0]["args"]["labels"] == ["foo"]

def test_payload():
    """Test using a 'real' payload."""
    hook = CommentLabelHook(
        get_payload('issue_comment_label.json'),
        whitelist=["foo"]
    )
    assert hook.should_perform_action(), "Issue comment with labels."

    actions = hook.actions()
    assert actions[0]["args"] == {
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/14",
        "labels": ["foo", "status: claimed"]
    }

def get_payload(input_filename):
    """Parse the JSON payload and return an object."""
    with open("tests/payloads/" + input_filename) as input_file:
        return json.load(input_file)
