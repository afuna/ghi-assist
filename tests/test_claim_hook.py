from ghi_assist.hooks.claim_hook import ClaimHook
import json

def test_claim():
    """Test successful claim."""
    hook = ClaimHook({
        "issue": {
            "assignee": None,
        },
        "comment": {
            "body": "So exciting. Claimed!"
        }
    })
    assert hook.should_perform_action(), "Claimed."

def test_no_claim_comment():
    """Test a comment with no special keywords."""
    hook = ClaimHook({
        "issue": {
            "assignee": None,
        },
        "comment": {
            "body": "Some comment here. Nothing special."
        }
    })
    assert not hook.should_perform_action(), "No-op"

def test_claim_assigned():
    """Test trying to claim something that's already assigned. (Assume user error)."""
    hook = ClaimHook({
        "issue": {
            "assignee": {},
        },
        "comment": {
            "body": "So exciting. Claimed!"
        }
    })
    assert not hook.should_perform_action(), "Already assigned."

def test_claim_payload():
    """Test claiming using a JSON payload. Just a double-check."""
    hook = ClaimHook(get_payload('issue_comment_unassigned.json'))
    assert hook.should_perform_action(), "Unassigned + 'claimed'."

    actions = hook.actions()
    assert actions[0]["args"] == {
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/14",
        "assignee": "user-foo",
    }

    assert actions[1]["args"] == {
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/14",
        "labels": []
    }

def get_payload(input_filename):
    """Parse the JSON payload and return an object."""
    with open("tests/payloads/" + input_filename) as input_file:
        return json.load(input_file)

