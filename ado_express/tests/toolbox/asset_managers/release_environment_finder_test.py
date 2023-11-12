import unittest
from unittest.mock import Mock, patch

from ado_express.packages.toolbox.asset_managers.release_environment_finder import \
    ReleaseEnvironmentFinder


class TestReleaseEnvironmentFinder(unittest.TestCase):

    def setUp(self):
        self.ms_auth_mock = Mock()
        self.env_vars_mock = Mock()
        self.env_vars_mock.RELEASE_TARGET_ENV = "target_env"
        self.release_environment_finder = ReleaseEnvironmentFinder(self.ms_auth_mock, self.env_vars_mock)

    def create_mock_release_environments(self, environment_names):
        mock_release = Mock()
        mock_release.environments = []

        for name in environment_names:
            new_environment = Mock()
            new_environment.name = name
            mock_release.environments.append(new_environment)

        return mock_release

    @patch('ado_express.packages.authentication.MSAuthentication')
    def test_get_release_environment(self, _):
        deployment_detail_mock = Mock(release_project_name='test_project')
        release_id = 123
        mock_release = self.create_mock_release_environments(['target_env'])
        self.ms_auth_mock.client.get_release.return_value = mock_release
        result = self.release_environment_finder.get_release_environment(deployment_detail_mock, release_id)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'target_env')

    @patch('ado_express.packages.authentication.MSAuthentication')
    def test_get_release_environments(self, _):
        deployment_detail_mock = Mock(release_project_name='test_project')
        release_id = 123
        mock_release = self.create_mock_release_environments(['env1', 'env2'])
        self.ms_auth_mock.client.get_release.return_value = mock_release

        result = self.release_environment_finder.get_release_environments(deployment_detail_mock, release_id)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, 'env1')   
        self.assertEqual(result[1].name, 'env2')

    @patch('ado_express.packages.authentication.MSAuthentication')
    def test_get_release_environment_by_id(self, _):
        project = 'test_project'
        release_id = 123
        environment_id = 456
        environment_mock = Mock()
        self.ms_auth_mock.client_v6.get_release_environment.return_value = environment_mock

        result = self.release_environment_finder.get_release_environment_by_id(project, release_id, environment_id)

        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
