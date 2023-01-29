import logging
from packages.common.enums import ReleaseEnvironmentStatuses
from packages.common.models.deployment_details import DeploymentDetails
from packages.utils.release_manager.update_release import UpdateRelease
from faker import Faker
from mock import patch
import unittest

class Empty:
    pass

class UpdateReleaseTests(unittest.TestCase):

    @patch('packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
    def test_update_release_env_notfound_should_fail(self, mock_update_release):
        # Arrange
        fake = Faker()
        deployment_details = DeploymentDetails(fake.name(), fake.name(), 123, 321, False)

        release_to_update = Empty()
        release_to_update.id = fake.random_int()

        mock_update_release.environment_variables = Empty()
        mock_update_release.environment_variables.RELEASE_TARGET_ENV = fake.name()

        failure_reason = f'Destination Release Environment "{mock_update_release.environment_variables.RELEASE_TARGET_ENV}" not found'

        # Act
        actual_result = UpdateRelease.update_release(mock_update_release, deployment_details, release_to_update)
        
        # Assert
        self.assertEqual(actual_result, (False, failure_reason)) 

    @patch('packages.utils.asset_retrievers.release_environment_finder.release_environment_finder.ReleaseEnvironmentFinder.get_release_environment', return_value=None)
    @patch('packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
    def test_update_release_already_updating_should_pass(self, mock_update_release, mock_get_release_environment):
        # Arrange
        fake = Faker()
        deployment_details = DeploymentDetails(fake.name(), fake.name(), 123, 321, False)

        release_to_update = Empty()
        release_to_update.id = fake.random_int()
        release_to_update.name = fake.name()

        mock_update_release.environment_variables = Empty()
        mock_update_release.environment_variables.RELEASE_TARGET_ENV = fake.name()

        matching_release_environment = Empty()
        matching_release_environment.status = ReleaseEnvironmentStatuses.InProgress.IN_PROGRESS
        
        mock_get_release_environment.return_value = matching_release_environment

        already_triggerd_log = [f'INFO:root:Release is already updating - Project:{deployment_details.release_project_name} Release Definition:{deployment_details.release_name} Release:{release_to_update.name} Environment:{mock_update_release.environment_variables.RELEASE_TARGET_ENV}']

        # Act  
        with self.assertLogs(level=logging.INFO) as cm:
            actual_result = UpdateRelease.update_release(mock_update_release, deployment_details, release_to_update)

        # Assert
        self.assertEqual(actual_result, (True, None))
        self.assertEqual(cm.output, already_triggerd_log)

    @patch('packages.utils.asset_retrievers.release_environment_finder.release_environment_finder.ReleaseEnvironmentFinder.get_release_environment', return_value=None)
    @patch('packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
    def test_update_release_triggered_should_pass(self, mock_update_release, mock_get_release_environment):
        # Arrange
        fake = Faker()
        deployment_details = DeploymentDetails(fake.name(), fake.name(), 123, 321, False)

        release_to_update = Empty()
        release_to_update.id = fake.random_int()
        release_to_update.name = fake.name()

        mock_update_release.environment_variables = Empty()
        mock_update_release.environment_variables.RELEASE_TARGET_ENV = fake.name()

        matching_release_environment = Empty()
        matching_release_environment.status = ReleaseEnvironmentStatuses.NotStarted.NOT_STARTED

        mock_get_release_environment.return_value = matching_release_environment

        update_triggered = [f'INFO:root:Update triggered - Project:{deployment_details.release_project_name} Release Definition:{deployment_details.release_name} Release:{release_to_update.name} Environment:{mock_update_release.environment_variables.RELEASE_TARGET_ENV}']

        # Act  
        with self.assertLogs(level=logging.INFO) as cm:
            actual_result = UpdateRelease.update_release(mock_update_release, deployment_details, release_to_update)

        # Assert
        self.assertEqual(actual_result, (True, None))
        self.assertEqual(cm.output, update_triggered)