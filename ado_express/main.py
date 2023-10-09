import logging
import os
import sys
import time

# Append current directory to sys.path for run-type isolation
sys.path.append(os.path.abspath("."))

from ado_express.packages.ado_express import ADOExpress
from ado_express.packages.shared import Constants, EnvironmentVariables
from ado_express.packages.toolbox import (DeploymentPlan, ExcelManager,
                                          run_helpers)

if __name__ == '__main__':
    constants = Constants()
    environment_variables = EnvironmentVariables()
    excel_manager = ExcelManager()
    ado_express = ADOExpress(environment_variables)
    deployment_details = None
    deployment_plan = DeploymentPlan(constants, environment_variables)
    run_start_time = time.perf_counter() 

    is_via_query_run = environment_variables.QUERIES is not None
    is_via_environment_latest_release_run = environment_variables.VIA_ENV_LATEST_RELEASE is not False

    deployment_details, user_provided_deployment_plan = run_helpers.get_deployment_details(
        deployment_plan, 
        ado_express, 
        is_via_query_run, 
        is_via_environment_latest_release_run
    )

    if environment_variables.SEARCH_ONLY:

        run_helpers.initiate_search(
            ado_express, 
            deployment_details, 
            is_via_query_run, 
            is_via_environment_latest_release_run, 
            user_provided_deployment_plan
        )

    elif run_helpers.have_deployable_releases(deployment_details, user_provided_deployment_plan) and run_helpers.user_confirmed_deployment():

        run_helpers.initiate_deployment(
            ado_express, 
            deployment_details, 
            user_provided_deployment_plan
        )
    else: 
        run_helpers.stop_process()

    run_end_time = time.perf_counter()
    logging.info(f'Tasks completed in {run_end_time-run_start_time} seconds.')