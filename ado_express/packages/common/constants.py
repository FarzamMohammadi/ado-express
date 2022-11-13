import os

class Constants:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DEPLOYMENT_PLAN_FILE_PATH = os.path.join(ROOT_DIR,'../../../files/deployment/deployment-plan.xlsx')
    LOG_FILE_PATH = os.path.join(ROOT_DIR,'../../../files/logs/deployment.log')
    SEARCH_RESULTS_FILE_PATH = os.path.join(ROOT_DIR,'../../../files/search-results/search-results.txt')
    SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH = os.path.join(ROOT_DIR,'../../../files/search-results/deployment-plan.xlsx')