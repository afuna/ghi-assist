from ghi_assist.utils import filter_by_claimed

def gh_labels(labels=None):
    """Transform an array of strings into an array of GH label object"""
    return [{"name": label} for label in labels]

def test_empty():
    """Test no labels to add/remove."""
    assert filter_by_claimed([], claimed=False) == ([], False)

def test_add_claim():
    """Test added 'status: claim' to an empty label list."""
    assert filter_by_claimed([], claimed=True) == (["status: claimed"], True)

def test_same_claim_status():
    """Test no duplicates when our label list already contains the current claimed status."""
    labels = ["bar", "foo", "status: claimed"]
    assert filter_by_claimed(gh_labels(labels), claimed=True) == \
        (["bar", "foo", "status: claimed"], False)

def test_toggle_claim_status():
    """Test no 'status: claimed' when we say that claimed is now False."""
    labels = ["bar", "foo", "status: claimed"]
    assert filter_by_claimed(gh_labels(labels), claimed=False) == (["bar", "foo"], True)
