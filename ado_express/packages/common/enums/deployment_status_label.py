from enum import Enum


class DeploymentStatusLabel(Enum):
    canceled = "Canceled"
    failed = "Failed"
    inProgress = "In Progress"
    notStarted = "Not Started"
    partiallySucceeded = "Partially Succeeded"
    queued = "Queued"
    rejected = "Rejected"
    scheduled = "Scheduled"
    succeeded = "Succeeded"
    undefined = "Undefined"
    notDeployed = "Initializing" # Default value for an environment or updating one that has not started yet (in our case most likely means initializing)