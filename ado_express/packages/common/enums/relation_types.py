from enum import Enum

class RelationTypes(str, Enum):
        COMMIT = 'commit'
        PULL_REQUEST_ID = 'pullrequestid'