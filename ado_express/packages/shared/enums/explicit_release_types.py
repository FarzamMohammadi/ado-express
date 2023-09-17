from enum import Enum

class ExplicitReleaseTypes(str, Enum):
        INCLUDE = 'include'
        EXCLUDE = 'exclude'