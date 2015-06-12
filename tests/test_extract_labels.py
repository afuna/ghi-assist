from ghi_assist.utils import extract_labels

def test_whitelist():
    """Test whitelist."""
    labels = extract_labels(
        "Hello ##category: label. ##label. ##unknown-label, ##valid-label",
        whitelist=["label", "valid-label", "category: label"]
    )
    assert labels == ["category: label", "label", "valid-label"]

def test_aliases():
    """Test aliases."""
    labels = extract_labels(
        "Hello ##category: label. ##label. ##unknown-label, ##valid-label",
        aliases={
            "category: label": "category: (1) sorted label",
            "label": "zzz this label is too long for me to type all the time",
            "valid-label": "valid label",
        }
    )
    assert labels == ["category: (1) sorted label",
                      "zzz this label is too long for me to type all the time",
                      "valid label",
                     ]

def test_no_whitelist():
    """Test no whitelist provided."""
    labels = extract_labels("Hello ##123")
    assert labels == []

def test_no_labels():
    """Test no labels in the text."""
    labels = extract_labels(
        "Hello world. This is issue #123 There's not actually a label in here for you.",
        whitelist=["123"]
    )
    assert labels == []
