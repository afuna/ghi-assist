from ghi_assist.hooks.assign_related_hook import AssignRelatedHook
import json
from mock import patch

def mock_issue_assignee(mockAPI, assignee=None):
    """Mock up a response for the issue API call."""
    instance = mockAPI.return_value
    instance.issue.return_value = {"assignee": assignee}

def mock_issue_response_payload(mockAPI):
    instance = mockAPI.return_value
    instance.issue.return_value = get_payload('issue_data.json')

@patch('ghi_assist.hooks.assign_related_hook.API')
def test_assign_from_title(mockAPI):
    """Test successful assignment, getting information from title."""
    mock_issue_assignee(mockAPI)
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
    assert hook.should_perform_action(payload), "Should assign"
    assert hook.related_issue_id == 123

@patch('ghi_assist.hooks.assign_related_hook.API')
def test_assign_from_body(mockAPI):
    """Test successful assignment, getting information from body."""
    mock_issue_assignee(mockAPI)
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
    assert hook.should_perform_action(payload), "Should assign"
    assert hook.related_issue_id == 456

@patch('ghi_assist.hooks.assign_related_hook.API')
def test_no_related(mockAPI):
    """Test no assignment, because we couldn't find a related issue."""
    mock_issue_assignee(mockAPI)
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
    assert not hook.should_perform_action(payload), "No related issue"
    assert hook.related_issue_id is None

@patch('ghi_assist.hooks.assign_related_hook.API')
def test_other_action(mockAPI):
    """Test no assignment, because we are doing something else to the pull request (e.g., closing)."""
    mock_issue_assignee(mockAPI)
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
    assert not hook.should_perform_action(payload), "Not PR open"
    assert hook.related_issue_id is None

@patch('ghi_assist.hooks.assign_related_hook.API')
def test_related_issue_assigned(mockAPI):
    """Test no assignment because the related issue was already assigned."""
    mock_issue_assignee(mockAPI, assignee="someone-else")
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
    assert not hook.should_perform_action(payload), "Assigning related issue after checking"
    assert hook.related_issue_id == 123

@patch('ghi_assist.hooks.assign_related_hook.API')
def test_payload(mockAPI):
    """Test assigning using a full payload."""
    mock_issue_response_payload(mockAPI)

    hook = AssignRelatedHook()
    payload = get_payload('pr_opened.json')
    assert hook.should_perform_action(payload), "PR opened"

    actions = hook.actions(payload)
    assert actions[0]["args"] == {
        "related_issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/999",
        "assignee": "user-foo",
    }

    assert actions[1]["args"] == {
        "related_issue_url": "https://api.github.com/repos/user-foo/repo-bar/issues/999",
        "labels": [],
    }

def get_payload(input_filename):
    """Parse the JSON payload and return an object."""
    with open("tests/payloads/" + input_filename) as input_file:
        return json.load(input_file)

