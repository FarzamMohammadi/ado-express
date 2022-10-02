from enum import Enum, EnumMeta

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

class BaseEnum(Enum, metaclass=MetaEnum):
        pass

class ENVIRONMENT_STATUSES:
    class IN_PROGRESS(BaseEnum):
        IN_PROGRESS = 'inProgress'
        NOT_STARTED = 'notStarted'
        QUEUED = 'queued'
        SCHEDULED = 'scheduled'

    class SUCCEEDED(BaseEnum):
        SUCCEEDED = 'succeeded'
        PARTIALLY_SUCCEEDED = 'partiallySucceeded'

    class FAILED(BaseEnum):
        CANCELED = 'canceled'
        REJECTED = 'rejected'
        UNDEFINED = 'undefined'
