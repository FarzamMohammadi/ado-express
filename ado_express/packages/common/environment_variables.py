import ast
import os
import re
import sys
import validators
from dotenv import load_dotenv

from packages.common.enums.explicit_release_types import ExplicitReleaseTypes

none_types = ["none", "null", "nill", " ", ""]

def get_validated_string_input(index, key, type=None, existing_value=None):
        if not existing_value:
            if len(sys.argv) > index and sys.argv[index] is not None:
                str_input = sys.argv[index].strip()
            elif os.getenv(key) is not None:
                str_input = os.getenv(key).strip()
            else: return None

            if not isinstance(str_input, str) or (str_input.strip().lower() in none_types):
                return None
            if type == "url":
                if not validators.url(str_input):
                    raise Exception(f"Invalid {key} provided.")
        else:
            str_input = existing_value

        if type == "query":
            if validators.url(str_input):
                try:
                    str_input = re.findall("[0-9A-Fa-f]{8}[-]?[0-9A-Fa-f]{4}[-]?[0-9A-Fa-f]{4}[-]?[0-9A-Fa-f]{4}[-]?[0-9A-Fa-f]{12}", str_input)[0] # If the entire query URL is passed get the ID from it
                except:
                    raise Exception(f"Invalid {key} provided.")
                
        return str_input

def get_validated_list_input(index, key):
        if len(sys.argv) > index and sys.argv[index] is not None:
            list_input = sys.argv[index].split(',')  
        elif os.getenv(key) is not None:
            list_input = os.getenv(key).split(',')
        else: return None

        if any(i.lower() in none_types for i in list_input) or not isinstance(list_input, list):
            return None

        if key=="QUERIES":
            query_list_input = []
            
            for query in list_input:
                query_list_input.append(get_validated_string_input(None, None, "query", query))
            
            list_input = query_list_input

        return list_input
def get_validated_bool_input(index, key):
        if len(sys.argv) > index and sys.argv[index] is not None:
            str_input = sys.argv[index].strip()
        elif os.getenv(key) is not None:
            str_input = os.getenv(key).strip()
        else: return False

        if str_input.strip().lower() in none_types:
            return False

        if str_input.lower() in ("true", "1", "t"):
            return True

def get_validated_object(index, key):
    if len(sys.argv) > index and sys.argv[index] is not None:
        str_input = sys.argv[index].strip()
    elif os.getenv(key) is not None:
        str_input = os.getenv(key).strip()
    else: return None

    return ast.literal_eval(str_input)           

class EnvironmentVariables:

    load_dotenv()

    EXPLICIT_RELEASE_VALUES = get_validated_object(1, "EXPLICIT_RELEASE_VALUES") # cmd arg 1
    CRUCIAL_RELEASE_DEFINITIONS = get_validated_list_input(2, "CRUCIAL_RELEASE_DEFINITIONS") # cmd arg 2
    ORGANIZATION_URL = get_validated_string_input(3, "ORGANIZATION_URL", "url") # cmd arg 3
    PERSONAL_ACCESS_TOKEN = get_validated_string_input(4, "PERSONAL_ACCESS_TOKEN") # cmd arg 4
    QUERIES = get_validated_list_input(5, "QUERIES") # cmd arg 5
    RELEASE_NAME_FORMAT = get_validated_string_input(6, "RELEASE_NAME_FORMAT") # cmd arg 6
    RELEASE_TARGET_ENV = get_validated_string_input(7, "RELEASE_TARGET_ENV") # cmd arg 7
    SEARCH_ONLY = get_validated_bool_input(8, "SEARCH_ONLY") # cmd arg 8
    VIA_ENV = get_validated_bool_input(9, "VIA_ENV") # cmd arg 9
    VIA_ENV_LATEST_RELEASE = get_validated_bool_input(10, "VIA_ENV_LATEST_RELEASE") # cmd arg 10
    VIA_ENV_SOURCE_NAME = get_validated_string_input(11, "VIA_ENV_SOURCE_NAME") # cmd arg 11

    if not SEARCH_ONLY and VIA_ENV and VIA_ENV_SOURCE_NAME is None:
        raise Exception("To deploy via stage you must provide a VIA_ENV_SOURCE_NAME")

    if (
        SEARCH_ONLY
        and VIA_ENV_LATEST_RELEASE
        and (VIA_ENV_SOURCE_NAME is None or RELEASE_TARGET_ENV is None)
    ):
        raise Exception("To search via stage latest release VIA_ENV_SOURCE_NAME & RELEASE_TARGET_ENV must be provided")

    if (
        SEARCH_ONLY
        and QUERIES
        and VIA_ENV
        and (VIA_ENV_SOURCE_NAME is None or RELEASE_TARGET_ENV is None)
    ):
        raise Exception("To search query via stage, VIA_ENV_SOURCE_NAME & RELEASE_TARGET_ENV must be provided")
    
    if EXPLICIT_RELEASE_VALUES:
        for key in EXPLICIT_RELEASE_VALUES:
            if key != ExplicitReleaseTypes.EXCLUDE and key != ExplicitReleaseTypes.INCLUDE:
                    raise Exception("Please select 'include' or 'exclude' as dictionary key for EXPLICIT_RELEASE_VALUES and provide releases in an array format in the dictionary value\n Example: {'include': ['release-1', 'release-2]}")
