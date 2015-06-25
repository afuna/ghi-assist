from ghi_assist.hooks.assign_related_hook import AssignRelatedHook
from ghi_assist.api import API
import json
from mock import patch, Mock

def test_assign_from_title():
    """Test successful assignment, getting information from title."""
    hook = AssignRelatedHook()
    payload = {
        "action": "opened",
        "pull_request": {
            "title": "[#123] Title",
            "body": "Some body",
        },
        "repository": {
            "issues_url": "https://api.github.com/repos/user-foo/repo-bar/issues{/number}"
        }
    }
    assert hook.related_issue_id is None
    with patch.object(API, 'issue') as mock_method:
        mock_method.return_value = {"assignee": None}
        assert hook.should_perform_action(payload, api=API()), "Should assign"
    assert hook.related_issue_id == 123

def test_assign_from_body():
    """Test successful assignment, getting information from body."""
    hook = AssignRelatedHook()
    payload = {
        "action": "opened",
        "pull_request": {
            "title": "Title",
            "body": "[#456] Some body",
        },
        "repository": {
            "issues_url": "https://api.github.com/repos/user-foo/repo-bar/issues{/number}"
        }
    }
    with patch.object(API, 'issue') as mock_method:
        mock_method.return_value = {"assignee": None}
        assert hook.should_perform_action(payload, api=API()), "Should assign"
    assert hook.related_issue_id == 456

def test_no_related():
    """Test no assignment, because we couldn't find a related issue."""
    hook = AssignRelatedHook()
    payload = {
        "action": "opened",
        "pull_request": {
            "title": "Title",
            "body": "Some body",
        },
        "repository": {
            "issues_url": "https://api.github.com/repos/user-foo/repo-bar/issues{/number}"
        }
    }
    with patch.object(API, 'issue') as mock_method:
        mock_method.return_value = {"assignee": None}
        assert not hook.should_perform_action(payload, api=API()), "No related issue"
    assert hook.related_issue_id is None

def test_other_action():
    """Test no assignment, because we are doing something else to the pull request (e.g., closing)."""
    hook = AssignRelatedHook()
    payload = {
        "action": "closed",
        "pull_request": {
            "title": "[#123] Title",
            "body": "Some body",
        },
        "repository": {
            "issues_url": "https://api.github.com/repos/user-foo/repo-bar/issues{/number}"
        }
    }
    with patch.object(API, 'issue') as mock_method:
        mock_method.return_value = {"assignee": None}
        assert not hook.should_perform_action(payload, api=API()), "Not PR open"
    assert hook.related_issue_id is None

def test_related_issue_assigned():
    """Test no assignment because the related issue was already assigned."""
    hook = AssignRelatedHook()
    payload = {
        "action": "opened",
        "pull_request": {
            "title": "[#123] Title",
            "body": "Some body",
        },
        "repository": {
            "issues_url": "https://api.github.com/repos/user-foo/repo-bar/issues{/number}"
        }
    }
    with patch.object(API, 'issue') as mock_method:
        mock_method.return_value = {"assignee": "someone-else"}
        assert not hook.should_perform_action(payload, api=API()), "Assigning related issue after checking"
    assert hook.related_issue_id == 123

def test_payload():
    """Test assigning using a full payload."""
    hook = AssignRelatedHook()
    payload = get_payload('pr_opened.json')

    with patch.object(API, 'issue') as mock_method:
        mock_method.return_value = get_payload('issue_data.json')
        assert hook.should_perform_action(payload, api=API()), "PR opened"
    actions = hook.actions(payload, Mock())
    assert actions[0]["args"] == {
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/999",
        "assignee": "user-foo",
    }

    assert actions[1]["args"] == {
        "issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/999",
        "labels": [],
    }

def get_payload(input_filename):
    """Parse the JSON payload and return an object."""
    with open("tests/payloads/" + input_filename) as input_file:
        return json.load(input_file)

