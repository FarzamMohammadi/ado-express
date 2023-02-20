class ReleaseDetails:
    """
    :param project_name:
    :type project_name: str
    :param release_name:
    :type release_name: str
    :param target_number:
    :type target_number: int
    :param rollback_number:
    :type rollback_number: int
    """
    def __init__(self, project_name: str, release_name: str, target_number: int, rollback_number: int):
        self.project_name = project_name
        self.release_name = release_name
        self.target_number = target_number
        self.rollback_number = rollback_number
    