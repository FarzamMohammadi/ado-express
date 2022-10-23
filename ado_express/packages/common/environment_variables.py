import os
from dotenv import load_dotenv

class EnvironmentVariables:

    load_dotenv()
    PERSONAL_ACCESS_TOKEN = os.getenv('PERSONAL_ACCESS_TOKEN')
    ORGANIZATION_URL = os.getenv('ORGANIZATION_URL')
    RELEASE_STAGE_NAME = os.getenv('RELEASE_STAGE_NAME')
    RELEASE_NAME_FORMAT = os.getenv('RELEASE_NAME_FORMAT')
    VIA_STAGE = os.getenv("VIA_STAGE", default='False').lower() in ('true', '1', 't')
    VIA_STAGE_SOURCE = None if os.getenv('VIA_STAGE_SOURCE') == '' else os.getenv('VIA_STAGE_SOURCE')
    SEARCH_ONLY = os.getenv("SEARCH_ONLY", default='False').lower() in ('true', '1', 't')
    
    if VIA_STAGE and VIA_STAGE_SOURCE is None:
        raise Exception('To use run VIA_STAGE you must provide a VIA_STAGE_SOURCE')