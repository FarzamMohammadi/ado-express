import os
import re
import sys
import validators
from dotenv import load_dotenv

none_types = ["none", "null", "nill", " ", ""]

def get_validated_string_input(index, key, type=None):
        if len(sys.argv) > index:
            str_input = sys.argv[index].strip()
        else:
            str_input = os.getenv(key).strip()

        if not isinstance(str_input, str) or (str_input.strip().lower() in none_types):
            return None
        else: 
            if type == "url":
                if not validators.url(str_input):
                    raise Exception(f"Invalid {key} provided.")
            if type == "query":
                if validators.url(str_input):
                    try:
                        str_input = re.findall("[0-9A-Fa-f]{8}[-]?[0-9A-Fa-f]{4}[-]?[0-9A-Fa-f]{4}[-]?[0-9A-Fa-f]{4}[-]?[0-9A-Fa-f]{12}", str_input)[0] # If the entire query URL is passed get the ID from it
                    except:
                        raise Exception(f"Invalid {key} provided.")
                
        return str_input

def get_validated_list_input(index, key):
        if len(sys.argv) > index:
            str_input = sys.argv[index].split(',')
        else:
            str_input = os.getenv(key).split(',')

        if any(i in str_input for i in none_types) or not isinstance(str_input, list):
            return None
        
        return str_input
def get_validated_bool_input(index, key):
        if len(sys.argv) > index:
            str_input = sys.argv[index].strip()
        else:
            str_input = os.getenv(key).strip()

        if str_input.strip().lower() in none_types:
            return False
        else: 
            if str_input.lower() in ("true", "1", "t"):
                return True
            return False
class EnvironmentVariables:

    load_dotenv()

    CRUCIAL_RELEASE_DEFINITIONS = get_validated_list_input(1, "CRUCIAL_RELEASE_DEFINITIONS") # cmd arg 1
    ORGANIZATION_URL = get_validated_string_input(2, "ORGANIZATION_URL", "url") # cmd arg 2
    PERSONAL_ACCESS_TOKEN = get_validated_string_input(3, "PERSONAL_ACCESS_TOKEN") # cmd arg 3
    QUERY = get_validated_string_input(4, "QUERY", "query") # cmd arg 4
    RELEASE_STAGE_NAME = get_validated_string_input(5, "RELEASE_STAGE_NAME") # cmd arg 5
    RELEASE_NAME_FORMAT = get_validated_string_input(6, "RELEASE_NAME_FORMAT") # cmd arg 6
    SEARCH_ONLY = get_validated_bool_input(7, "SEARCH_ONLY") # cmd arg 7
    VIA_STAGE = get_validated_bool_input(8, "VIA_STAGE") # cmd arg 8
    VIA_STAGE_SOURCE_NAME = get_validated_string_input(9, "VIA_STAGE_SOURCE_NAME") # cmd arg 9
    VIA_STAGE_LATEST_RELEASE = get_validated_bool_input(10, "VIA_STAGE_LATEST_RELEASE") # cmd arg 10

    if not SEARCH_ONLY and VIA_STAGE and VIA_STAGE_SOURCE_NAME is None:
        raise Exception("To deploy via stage you must provide a VIA_STAGE_SOURCE_NAME")

    if (
        SEARCH_ONLY
        and VIA_STAGE_LATEST_RELEASE
        and (VIA_STAGE_SOURCE_NAME is None or RELEASE_STAGE_NAME is None)
    ):
        raise Exception(
            "To search via stage latest release VIA_STAGE_SOURCE_NAME & RELEASE_STAGE_NAME must be provided"
        )

    if (
        SEARCH_ONLY
        and QUERY
        and VIA_STAGE
        and (VIA_STAGE_SOURCE_NAME is None or RELEASE_STAGE_NAME is None)
    ):
        raise Exception(
            "To search query via stage, VIA_STAGE_SOURCE_NAME & RELEASE_STAGE_NAME must be provided"
        )
