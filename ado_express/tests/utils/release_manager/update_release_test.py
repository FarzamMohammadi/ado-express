import logging
import unittest

from faker import Faker
from mock import patch

from ado_express.packages.shared.enums import ReleaseEnvironmentStatuses
from ado_express.packages.shared.models.deployment_details import \
    DeploymentDetails
from ado_express.packages.toolbox.release_manager.update_release import \
    UpdateRelease


class Empty:
    pass

class UpdateReleaseTests(unittest.TestCase):
    @patch('ado_express.packages.utils.release_manager.update_release.UpdateRelease.release_client.get_release', return_value=None)
    @patch('ado_express.packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
    def test_get_release_update_result(self, mock_update_release, mock_release_client):
        # Arrange
        fake = Faker()

        deployment_detail = Empty()
        deployment_detail.release_project_name = fake.name()

        release_to_update = Empty()
        release_to_update.id = fake.name()

        mock_update_release.environment_variables = Empty()
        mock_update_release.environment_variables.RELEASE_TARGET_ENV = fake.name()

        updated_release_environment = Empty()
        updated_release_environment.name = mock_update_release.environment_variables.RELEASE_TARGET_ENV
        updated_release_environment.status = ReleaseEnvironmentStatuses.Succeeded.SUCCEEDED

        updated_deployment_details = Empty()
        updated_deployment_details.environments = [updated_release_environment]

        mock_release_client.return_value = updated_deployment_details

        # Act
        actual_result = UpdateRelease.get_release_update_result(mock_update_release, deployment_detail, release_to_update)
        
        # Assert
        self.assertTrue(actual_result)

    @patch('ado_express.packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
    def test_handle_failed_update_crucial(self, mock_update_release):
        # Arrange
        fake = Faker()
        failure_reason = fake.name()
        deployment_detail = DeploymentDetails(fake.name(), fake.name(), 123, 321, True)
        exception_message = 'A crucial release update failed. Roll back was attempted. Now, stopping the process.'
        
        # Act
        with self.assertRaises(Exception) as context:
            UpdateRelease.handle_failed_update(mock_update_release, deployment_detail, False, failure_reason)     
        
        # Assert
        self.assertTrue(exception_message in str(context.exception))

    @patch('ado_express.packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
    def test_handle_failed_update_noncrucial(self, mock_update_release):
        # Arrange
        fake = Faker()
        deployment_detail = DeploymentDetails(fake.name(), fake.name(), 123, 321, False)

        noncrucial_message = [f'ERROR:root:Release Update Unsuccessful - Reason: Please check logs - Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name}', 
                              f'INFO:root:The failed release update was not crucial. Continuing... Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name}']
        
        # Act
        with self.assertLogs(level=logging.INFO) as cm:
            UpdateRelease.handle_failed_update(mock_update_release, deployment_detail)     
        # Assert
        self.assertEqual(cm.output, noncrucial_message)

    @patch('ado_express.packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
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

    @patch('ado_express.packages.utils.asset_retrievers.release_environment_finder.release_environment_finder.ReleaseEnvironmentFinder.get_release_environment', return_value=None)
    @patch('ado_express.packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
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

    @patch('ado_express.packages.utils.asset_retrievers.release_environment_finder.release_environment_finder.ReleaseEnvironmentFinder.get_release_environment', return_value=None)
    @patch('ado_express.packages.utils.release_manager.update_release.UpdateRelease', return_value=None)
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