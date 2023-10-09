from ado_express.packages.toolbox.run_helpers import needs_deployment


def test_needs_deployment():
    target = 155
    rollback = 160
    assert needs_deployment(target, rollback) == False