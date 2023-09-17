from enum import Enum
from .meta_enum import MetaEnum

class BaseEnum(Enum, metaclass=MetaEnum):
    pass