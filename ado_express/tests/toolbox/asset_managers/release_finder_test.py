import unittest
from unittest.mock import Mock, patch

from ado_express.packages.toolbox import ReleaseFinder


class TestReleaseFinder(unittest.TestCase):

    def setUp(self):
        self.ms_auth_mock = Mock()
        self.ms_auth_mock.release_client = Mock()
        self.env_vars_mock = Mock()
        self.release_finder = ReleaseFinder(self.ms_auth_mock, self.env_vars_mock)

    def create_mock_releases(self, release_names):
        mock_releases = []

        for name in release_names:
            mock_release = Mock()
            mock_release.name = name
            mock_releases.append(mock_release)

        return mock_releases

    def test_find_matching_release_via_name(self):
        releases = self.create_mock_releases(['Release-1', 'Release-2', 'Release-3'])
        self.env_vars_mock.RELEASE_NAME_FORMAT = 'Release-$(rev:r)'
        release_number = 2

        result = self.release_finder.find_matching_release_via_name(releases, release_number)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'Release-2')

    def test_find_matching_releases_via_name(self):
        releases = [Mock(id=1, name='Release1'), Mock(id=2, name='Release2')]
        release_number = 1
        deployment_detail = Mock(release_project_name='Project1')
        self.env_vars_mock.RELEASE_NAME_FORMAT = "Release-$(rev:r)"
        mock_environment = Mock(name="Stage1", status="Succeeded")
        mock_release = Mock()
        mock_release.environments = [mock_environment]
        self.release_client.get_release.return_value = mock_release

        result = self.release_finder.find_matching_releases_via_name(releases, release_number, deployment_detail)

        self.assertTrue(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].release_name, 'Release1')


    # def test_find_matching_release_via_source_stage(self):
    #     releases = [Mock(id=1, name='Release1'), Mock(id=2, name='Release2')]
    #     deployment_detail = 'Project1/Release1'
    #     self.env_vars_mock.RELEASE_TARGET_ENV = "Stage1"
    #     mock_environment = Mock(name="Stage1", status="Succeeded")
    #     mock_release = Mock()
    #     mock_release.environments = [mock_environment]
    #     self.release_client.get_release.return_value = mock_release

    #     result = self.release_finder.find_matching_release_via_source_stage(releases, deployment_detail)

    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.name, 'Release1')

    # def test_find_matching_releases_via_env(self):
    #     releases = [Mock(id=1, name='Release1'), Mock(id=2, name='Release2')]
    #     deployment_detail = Mock(release_project_name='Project1')
    #     self.env_vars_mock.RELEASE_TARGET_ENV = "Stage1"
    #     mock_environment = Mock(name="Stage1", status="Succeeded")
    #     mock_release = Mock()
    #     mock_release.environments = [mock_environment]
    #     self.release_client.get_release.return_value = mock_release

    #     result = self.release_finder.find_matching_releases_via_env(releases, deployment_detail)

    #     self.assertTrue(result)
    #     self.assertEqual(len(result), 1)
    #     self.assertEqual(result[0].release_name, 'Release1')


    # def test_get_release(self):
    #     deployment_detail = Mock(release_project_name='Project1', release_name='Release1', release_number=1)
    #     self.release_client.get_release_definitions.return_value.value = [Mock(name='Release1', id=123)]
    #     self.release_client.get_releases.return_value.value = [Mock(id=1, name='Release1.0')]
    #     self.env_vars_mock.RELEASE_NAME_FORMAT = "Release-$(rev:r)"

    #     result = self.release_finder.get_release(deployment_detail)

    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.name, 'Release1.0')

    # def test_get_releases(self):
    #     deployment_detail = Mock(release_project_name='Project1', release_name='Release1', release_number=1)
    #     self.release_client.get_release_definitions.return_value.value = [Mock(name='Release1', id=123)]
    #     self.release_client.get_releases.return_value.value = [Mock(id=1, name='Release1.0')]
    #     self.env_vars_mock.RELEASE_NAME_FORMAT = "Release-$(rev:r)"

    #     result = self.release_finder.get_releases(deployment_detail)

    #     self.assertTrue(result)
    #     self.assertEqual(len(result), 1)
    #     self.assertEqual(result[0].release_name, 'Release1.0')

    # def test_get_releases_dict_from_build_releases(self):
    #     release = Mock(project_reference=Mock(name='Project1'), release_definition=Mock(name='ReleaseDef'), name='Release1', id=1)
    #     self.env_vars_mock.VIA_ENV_SOURCE_NAME = "Stage1"
    #     mock_environment = Mock(name="Stage1", status="Succeeded")
    #     mock_release = Mock()
    #     mock_release.environments = [mock_environment]
    #     self.release_client.get_release.return_value = mock_release

    #     result = self.release_finder.get_releases_dict_from_build_releases(release, 'Release-')

    #     self.assertIsNotNone(result)
    #     self.assertIn('Project1/ReleaseDef', result)

    # def test_get_releases_from_build_id(self):
    #     build_id = 123
    #     mock_release = Mock(description="Test Build", project_reference=Mock(name='Project1'))
    #     self.release_client.get_releases.return_value.value = [mock_release]
    #     self.build_client.get_build.return_value = Mock(definition=Mock(name="Test Build"))

    #     result = self.release_finder.get_releases_from_build_id(build_id)

    #     self.assertIsNotNone(result)
    #     self.assertTrue(result)

    # def test_get_releases_via_builds(self):
    #     build_ids = [123, 456]
    #     mock_release = Mock(project_reference=Mock(name='Project1'), release_definition=Mock(name='ReleaseDef'), name='Release1', id=1)
    #     self.release_client.get_releases.return_value.value = [mock_release]
    #     self.build_client.get_build.return_value = Mock(definition=Mock(name="Test Build"))
    #     self.env_vars_mock.VIA_ENV_SOURCE_NAME = "Stage1"
    #     mock_environment = Mock(name="Stage1", status="Succeeded")
    #     mock_release_get = Mock()
    #     mock_release_get.environments = [mock_environment]
    #     self.release_client.get_release.return_value = mock_release_get

    #     result = self.release_finder.get_releases_via_builds(build_ids, 'Release-')

    #     self.assertIsNotNone(result)
    #     self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()