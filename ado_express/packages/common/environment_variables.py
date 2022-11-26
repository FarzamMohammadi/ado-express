import os
import sys
from dotenv import load_dotenv

class EnvironmentVariables:

    load_dotenv()
    ORGANIZATION_URL = os.getenv('ORGANIZATION_URL') or sys.argv[1] if len(sys.argv) > 1 else None # argument 1
    PERSONAL_ACCESS_TOKEN = os.getenv('PERSONAL_ACCESS_TOKEN') or sys.argv[2] if len(sys.argv) > 2 else None # argument 2
    QUERY = os.getenv('QUERY') or sys.argv[3] if len(sys.argv) > 3 else None # argument 3
    RELEASE_STAGE_NAME = os.getenv('RELEASE_STAGE_NAME') or sys.argv[4] if len(sys.argv) > 4 else None # argument 4
    RELEASE_NAME_FORMAT = os.getenv('RELEASE_NAME_FORMAT') or sys.argv[5] if len(sys.argv) > 5 else None # argument 5
    SEARCH_ONLY = os.getenv("SEARCH_ONLY", default='False').lower() in ('true', '1', 't') or sys.argv[6].lower() in ('true', '1', 't') if len(sys.argv) > 6 else False # argument 6
    VIA_STAGE = os.getenv("VIA_STAGE", default='False').lower() in ('true', '1', 't') or sys.argv[7].lower() in ('true', '1', 't') if len(sys.argv) > 7 else False # argument 7
    VIA_STAGE_SOURCE_NAME = None if os.getenv('VIA_STAGE_SOURCE_NAME') == '' else os.getenv('VIA_STAGE_SOURCE_NAME') or sys.argv[1] if len(sys.argv) > 8 else None # argument 8
    VIA_STAGE_LATEST_RELEASE = os.getenv("VIA_STAGE_LATEST_RELEASE", default='False').lower() in ('true', '1', 't') or sys.argv[9].lower() in ('true', '1', 't') if len(sys.argv) > 9 else False # argument 9

    if not SEARCH_ONLY and VIA_STAGE and VIA_STAGE_SOURCE_NAME is None:
        raise Exception('To deploy via stage you must provide a VIA_STAGE_SOURCE_NAME')
    
    if SEARCH_ONLY and VIA_STAGE_LATEST_RELEASE and (VIA_STAGE_SOURCE_NAME is None or RELEASE_STAGE_NAME is None):
        raise Exception('To search via stage latest release VIA_STAGE_SOURCE_NAME & RELEASE_STAGE_NAME must be provided')

    if SEARCH_ONLY and QUERY and VIA_STAGE and (VIA_STAGE_SOURCE_NAME is None or RELEASE_STAGE_NAME is None):
        raise Exception('To search query via stage VIA_STAGE_SOURCE_NAME & RELEASE_STAGE_NAME must be provided')
