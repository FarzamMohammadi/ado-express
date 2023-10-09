import concurrent.futures
import logging
import sys

from ado_express.packages.shared import Constants
from ado_express.packages.toolbox import ExcelManager

constants = Constants()
excel_manager = ExcelManager()
        
def user_confirmed_deployment():
    user_input = input("Are you sure you want to deploy the releases? (Y/N): ").strip().lower()
    return user_input in ["yes", "y"]

def stop_process():
    logging.info(f'Stopping process :(')
    exit()

def is_running_as_executable(): return getattr(sys, 'frozen', False)

def get_deployment_details(deployment_plan, ado_express, is_query_run, is_via_environment_latest_release_run):
    deployment_details = user_provided_deployment_plan = None

    if is_query_run:
        deployment_details = ado_express.get_deployment_details_from_query()
    else:
        user_provided_deployment_plan = deployment_plan.get_data_from_deployment_plan_file()

        if is_via_environment_latest_release_run:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                deployment_details = executor.map(ado_express.get_deployment_detail_from_latest_release, user_provided_deployment_plan)
    
    return deployment_details, user_provided_deployment_plan

def have_deployable_releases(deployment_details, user_provided_deployment_plan):
      return (deployment_details is not None and any(True for _ in deployment_details)) or len(user_provided_deployment_plan)

def initiate_search(ado_express, deployment_details, is_query_run, is_via_environment_latest_release_run, user_provided_deployment_plan):
    if not is_running_as_executable():
        if is_query_run or is_via_environment_latest_release_run:
            if deployment_details:
                logging.info(f'Exporting Release notes to: {constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH}')

                ado_express.prepare_result_excel_file()

                export_results_to_excel_file(deployment_details)
            else:
                logging.info(f'No results found - please check the configuration')
        else:    
            for deployment_detail in user_provided_deployment_plan:
                ado_express.search_and_log_details_only(deployment_detail)

def export_results_to_excel_file(deployment_details):
    for deployment_detail in deployment_details:
        if deployment_detail is not None: # The ThreadPoolExecutor may return None for some releases
            row = excel_manager.convert_deployment_detail_to_excel_row(constants.DEPLOYMENT_PLAN_HEADERS, deployment_detail)
            excel_manager.save_or_concat_file(row, constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH)

def initiate_deployment(ado_express, deployment_details, user_provided_deployment_plan):
    deployment_details = prepare_deployable_release_details(ado_express, deployment_details, user_provided_deployment_plan)
        
    crucial_deployment_details, regular_deployment_details = separate_regular_and_crucial_releases(ado_express, deployment_details)

    if crucial_deployment_details: deploy_crucial_releases(ado_express, crucial_deployment_details)

    if regular_deployment_details: deploy_regular_releases(ado_express, regular_deployment_details, crucial_deployment_details)

def prepare_deployable_release_details(ado_express, deployment_details, user_provided_deployment_plan):
    # When running a query/via-latest-environment-release, deployment_details will be none
    deployment_details = user_provided_deployment_plan if deployment_details is None else deployment_details

    deployment_details = ado_express.updated_deployment_details_based_on_explicit_inclusion_and_exclusion(deployment_details)

    if deployment_details is None:
        logging.error(f'No deployment details found - please check the configurations')
        stop_process()

    return deployment_details

def separate_regular_and_crucial_releases(ado_express, deployment_details):
    crucial_release_definitions = ado_express.get_crucial_release_definitions(deployment_details)
    crucial_deployment_details = []

    if crucial_release_definitions:
            # Separate crucial & regular deployments based on release definitions that match CRUCIAL_RELEASE_DEFINITIONS env variable list
        crucial_deployment_details = ado_express.get_crucial_deployment_from_deployment_details(deployment_details, crucial_release_definitions)
        deployment_details[:] = ado_express.remove_crucial_deployments_from_deployment_details(deployment_details, crucial_release_definitions)
    
    return crucial_deployment_details, deployment_details

def deploy_crucial_releases(ado_express, crucial_deployment_details):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        logging.info('Initiating deployment, beginning with critical releases.')
                
        executor.map(ado_express.deploy_to_target_or_rollback, crucial_deployment_details)
        executor.shutdown(wait=True)

def deploy_regular_releases(ado_express, deployment_details, crucial_deployment_details):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if crucial_deployment_details: 
            logging.info('Deploying the rest of the releases.')
        else:
            logging.info('Deploying releases.')
            
        executor.map(ado_express.deploy_to_target_or_rollback, deployment_details)

def needs_deployment(target_release_number, rollback_release_number): return int(target_release_number) > int(rollback_release_number)