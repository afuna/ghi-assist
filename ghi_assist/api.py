"""
Interface with the Github API
"""
import requests
import json
from .utils import filter_by_claimed

class API(object):
    def __init__(self, token=None, useragent="GHI Assist"):
        self.token = token
        self.useragent = useragent

    def _call(self, api_url, content=None, method="PUT"):
        """
        Convenience method which calls the Github API with default arguments.

        Args:
            api_url: URL of API endpoint.
            content (optional): dictionary of content.
            method (optional): HTTP method. Defaults to "PUT".
        Returns:
            The response object.
        """
        headers = {
            'User-Agent': self.useragent,
            'Authorization': "token %s" % self.token,
        }
        response = requests.request(method, api_url, headers=headers, data=json.dumps(content))
        return response.json()

    def assign_issue(self, issue_url=None, assignee=None):
        """
        Assigns an issue to the given user.

        Args:
            issue_url: API endpoint for this issue.
            assignee: String with the user's login username.
        """
        return self._call(issue_url, content={"assignee": assignee}, method="PATCH")

    def label_claimed(self, issue_url=None, labels=None):
        """
        Replace the list of labels if we've changed the issue's claimed status
        """
        new_labels, replace = filter_by_claimed(labels, claimed=True)
        if replace:
            return self._call("%s/labels" % issue_url, content=new_labels)

    def issue(self, issue_url=None):
        """
        Get issue data.

        Args:
            issue_url: url for the issue we're getting data for.
        Returns:
            The issue data as a dictionary.
        """
        return self._call(issue_url, method="GET")

    def add_labels(self, issue_url, labels=None):
        """
        Add issue labels (while keeping existing ones).

        Args:
            issue_url: API endpoint for this issue.
            labels: list of labels to add.
        """
        if len(labels) > 0:
            return self._call("%s/labels" % issue_url, content=labels, method="POST")


    def replace_labels(self, issue_url=None, labels=None):
        """
        Replace issue labels.

        Args:
            issue_url: API endpoint for this issue. Taken from previous API response.
            labels: list of labels to use.
        """
        if len(labels) > 0:
            return self._call("%s/labels" % issue_url, content=labels)

    def get_repo_labels(self, labels_url=None):
        """
        Get labels for a repository.

        Args:
            labels_url: API endpoint for labels for this repository
        """
        return self._call(labels_url, method="GET")

