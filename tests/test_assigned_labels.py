from ghi_assist.hooks.assigned_label_hook import AssignedLabelHook

def test_assign():
    """Test successful assignment."""
    hook = AssignedLabelHook()
    payload = {"action": "assigned",
               "issue": {"labels": [{"name": "alpha"},
                                    {"name": "beta"},
                                    {"name": "gamma"}]}}
    assert hook.should_perform_action(payload), "Need to perform action"
    assert len(hook.labels) == 4, "Should be four labels"
    assert "status: claimed" in hook.labels, "Needs to be claimed"

def test_unassign():
    """Test successful unassignment."""
    hook = AssignedLabelHook()
    payload = {"action": "unassigned",
               "issue": {"labels": [{"name": "alpha"},
                                    {"name": "beta"},
                                    {"name": "gamma"},
                                    {"name": "status: claimed"}]}}
    assert hook.should_perform_action(payload), "Needs to perform action"
    assert len(hook.labels) == 3, "Should be three labels"
    assert "status: claimed" not in hook.labels, "Needs to be unclaimed"

def test_unneeded_assign():
    """Test unnecessary assignment."""
    hook = AssignedLabelHook()
    payload = {"action": "assigned",
               "issue": {"labels": [{"name": "alpha"},
                                    {"name": "beta"},
                                    {"name": "gamma"},
                                    {"name": "status: claimed"}]}}
    assert not hook.should_perform_action(payload), "No need to perform action"
    assert len(hook.labels) == 4, "Should be four labels"
    assert "status: claimed" in hook.labels, "Needs to be claimed"

def test_unneeded_unassign():
    """Test unnecessary unassignment."""
    hook = AssignedLabelHook()
    payload = {"action": "unassigned",
               "issue": {"labels": [{"name": "alpha"},
                                    {"name": "beta"},
                                    {"name": "gamma"}]}}
    assert not hook.should_perform_action(payload), "No need to perform action"
    assert len(hook.labels) == 3, "Should be three labels"
    assert "status: claimed" not in hook.labels, "Needs to be unclaimed"
