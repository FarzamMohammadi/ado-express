from ado_express.packages.utils.release_note_helpers import needs_deployment


def test_needs_deployment():
    target = 155
    rollback = 160
    assert needs_deployment(target, rollback) == False