from .base_enum import BaseEnum


class ReleaseEnvironmentStatuses:
    class InProgress(BaseEnum):
        IN_PROGRESS = 'inProgress'

    class Succeeded(BaseEnum):
        SUCCEEDED = 'succeeded'
        PARTIALLY_SUCCEEDED = 'partiallySucceeded'
        
    class NotStarted(BaseEnum):
        NOT_STARTED = 'notStarted'
        QUEUED = 'queued'
        SCHEDULED = 'scheduled'

    class Failed(BaseEnum):
        FAILED = 'failed'
        CANCELED = 'canceled'
        REJECTED = 'rejected'
    
    class Undefined(BaseEnum):
        UNDEFINED = 'undefined'