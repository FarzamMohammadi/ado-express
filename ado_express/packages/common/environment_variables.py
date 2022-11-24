import os
from dotenv import load_dotenv

class EnvironmentVariables:

    load_dotenv()
    ORGANIZATION_URL = os.getenv('ORGANIZATION_URL')
    PERSONAL_ACCESS_TOKEN = os.getenv('PERSONAL_ACCESS_TOKEN')
    QUERY = os.getenv('QUERY')
    RELEASE_STAGE_NAME = os.getenv('RELEASE_STAGE_NAME')
    RELEASE_NAME_FORMAT = os.getenv('RELEASE_NAME_FORMAT')
    SEARCH_ONLY = os.getenv("SEARCH_ONLY", default='False').lower() in ('true', '1', 't')
    VIA_STAGE = os.getenv("VIA_STAGE", default='False').lower() in ('true', '1', 't')
    VIA_STAGE_SOURCE_NAME = None if os.getenv('VIA_STAGE_SOURCE_NAME') == '' else os.getenv('VIA_STAGE_SOURCE_NAME')
    VIA_STAGE_LATEST_RELEASE = os.getenv("VIA_STAGE_LATEST_RELEASE", default='False').lower() in ('true', '1', 't')
    
    if not SEARCH_ONLY and VIA_STAGE and VIA_STAGE_SOURCE_NAME is None:
        raise Exception('To use run VIA_STAGE you must provide a VIA_STAGE_SOURCE_NAME')