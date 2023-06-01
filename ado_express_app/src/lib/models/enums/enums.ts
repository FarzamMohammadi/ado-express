export enum ToastType {
    Success = 'success',
    Warning = 'warning',
    Error = 'danger',
    Info = 'default',
}

export enum RunType {
    Search = 'Search',
    Deploy = 'Deploy'
}

export enum SearchRunMethod {
    ViaEnvironment = 'Via Release Environment',
    ViaLatestInEnvironment = 'Via Latest in Environment',
    ViaNumber = "Via Release Number",
    ViaQuery = "Via ADO Query"
}

export enum DeploymentRunMethod {
    ViaNumber = "Via Release Number"
}

export enum WebsocketMessageType {
    Generic = "Generic",
    DeploymentStatus = "DeploymentStatus",
    SearchStatus = "SearchStatus",
    Error = "Error",
}