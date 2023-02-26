class DeploymentDetails:
    """
    :param release_project_name:
    :type release_project_name: str
    :param release_name:
    :type release_name: str
    :param release_number:
    :type release_number: int
    :param release_rollback:
    :type release_rollback: int
    :param is_crucial:
    :type is_crucial: bool
    """
    def __init__(self, release_project_name: str, release_name: str, release_number: int, release_rollback: int, is_crucial: bool):
        self.release_project_name = release_project_name
        self.release_name = release_name
        self.release_number = release_number
        self.release_rollback = release_rollback
        self.is_crucial = is_crucial
    