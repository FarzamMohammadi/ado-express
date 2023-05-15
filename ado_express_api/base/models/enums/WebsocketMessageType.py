from enum import Enum


class WebsocketMessageType(Enum):
    Generic = "Generic"
    DeploymentStatus = "DeploymentStatus"
    SearchResults = "SearchStatus"
    Error = "Error"
