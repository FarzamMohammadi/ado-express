import os
import sys
from dotenv import load_dotenv

class EnvironmentVariables:

    load_dotenv()
    ORGANIZATION_URL = (
        os.getenv("ORGANIZATION_URL")
        if os.getenv("ORGANIZATION_URL") is not None
        else sys.argv[1]
            if len(sys.argv) > 1
            else None
    )  # cmd arg 1
    PERSONAL_ACCESS_TOKEN = (
        os.getenv("PERSONAL_ACCESS_TOKEN")
        if os.getenv("PERSONAL_ACCESS_TOKEN") is not None
        else sys.argv[2]
            if len(sys.argv) > 2
            else None
    )  # cmd arg 2
    QUERY = (
        os.getenv("QUERY")
        if os.getenv("QUERY") is not None
        else sys.argv[3]
            if len(sys.argv) > 3
            else None
    )  # cmd arg 3
    RELEASE_STAGE_NAME = (
        os.getenv("RELEASE_STAGE_NAME")
        if os.getenv("RELEASE_STAGE_NAME") is not None
        else sys.argv[4]
            if len(sys.argv) > 4
            else None
    )  # cmd arg 4
    RELEASE_NAME_FORMAT = (
        os.getenv("RELEASE_NAME_FORMAT")
        if os.getenv("RELEASE_NAME_FORMAT") is not None
        else sys.argv[5]
            if len(sys.argv) > 5
            else None
    )  # cmd arg 5
    SEARCH_ONLY = (
        os.getenv("SEARCH_ONLY", default="False").lower() in ("true", "1", "t")
        if os.getenv("SEARCH_ONLY") is not None
        else sys.argv[6].lower() in ("true", "1", "t")
            if len(sys.argv) > 6
            else False
    )  # cmd arg 6
    VIA_STAGE = (
        os.getenv("VIA_STAGE", default="False").lower() in ("true", "1", "t")
        if os.getenv("VIA_STAGE") is not None
        else sys.argv[7].lower() in ("true", "1", "t")
            if len(sys.argv) > 7
            else False
    )  # cmd arg 7
    VIA_STAGE_SOURCE_NAME = (
        os.getenv("VIA_STAGE_SOURCE_NAME")
        if os.getenv("VIA_STAGE_SOURCE_NAME") is not None
        else sys.argv[8]
            if len(sys.argv) > 8
            else None
    )  # cmd arg 8
    VIA_STAGE_LATEST_RELEASE = (
        os.getenv("VIA_STAGE_LATEST_RELEASE", default="False").lower()
        in ("true", "1", "t")
        if os.getenv("VIA_STAGE_LATEST_RELEASE") is not None
        else sys.argv[9].lower() in ("true", "1", "t")
            if len(sys.argv) > 9
            else False
    )  # cmd arg 9
    CRUCIAL_RELEASE_DEFINITIONS = (
        os.getenv("CRUCIAL_RELEASE_DEFINITIONS").split(",")
        if os.getenv("CRUCIAL_RELEASE_DEFINITIONS") is not None
        else sys.argv[10].split(",")
            if len(sys.argv) > 10
            else None
    )  # cmd arg 10
    USE_SEARCH_RESULTS = (
        os.getenv("USE_SEARCH_RESULTS", default="False").lower() in ("true", "1", "t")
        if os.getenv("USE_SEARCH_RESULTS") is not None
        else sys.argv[11].lower() in ("true", "1", "t")
            if len(sys.argv) > 11
            else False
    )  # cmd arg 11

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
            "To search query via stage VIA_STAGE_SOURCE_NAME & RELEASE_STAGE_NAME must be provided"
        )
