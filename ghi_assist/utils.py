"""
Miscellaneous utility functions for labels.
"""
import re

LABEL_PATTERN = re.compile(r"""\#\#(?P<label>
                                (?:
                                    \w          # word character
                                    |
                                    [-]         # any non-word characters we accept
                                    |
                                    (?:
                                        :[ ]    # colon followed by a space
                                    )
                                )+)
                            """, re.VERBOSE)

def filter_by_claimed(github_labels, claimed=False):
    """
    Toggle the 'status: claimed' label depending on claimed status.

    Args:
        github_labels: List of Github labels as dicts (not strings)
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

def extract_labels(text, whitelist=None, aliases=None):
    """
    Extract potential labels from the text.

    Args:
        text: string to search for labels in the form of "##label" "##prefix: label".
        whitelist (optional): a list of labels to accept.
        aliases (optional): a dict of label aliases. Aliases can be used for long labels, or for
            labels with spaces.
    Returns:
        List of label names in the order they appeared in the text.
    """
    if whitelist is None:
        whitelist = []
    if aliases is None:
        aliases = {}

    valid_labels = aliases.copy()
    for label in whitelist:
        valid_labels[label] = label

    labels = []
    matches = LABEL_PATTERN.findall(text)
    for match in matches:
        if match in valid_labels:
            labels.append(valid_labels[match])

    return labels
