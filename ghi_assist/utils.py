"""
Miscellaneous utility functions for labels.
"""

def filter_by_claimed(github_labels, claimed=False):
    """
    Take a list of labels and toggle the 'status: claimed' label depending on claimed status.

    Args:
        github_labels: List of Github label objects
        claimed: True if issue should be claimed; False if it shouldn't be
    Returns:
        A tuple of:
        * sorted list of label names as strings.
        * True/False if we should replace the previous list with the current one.
    """
    labels_set = set([l["name"] for l in github_labels])
    original_len = len(labels_set)

    if claimed:
        labels_set.add("status: claimed")
    else:
        labels_set.discard("status: claimed")

    # So we don't have unnecessary API calls, only try to replace labels if the list has changed
    replace = False
    if original_len != len(labels_set):
        replace = True
    results = sorted(list(labels_set))
    return (results, replace)
