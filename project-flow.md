'''mermaid
graph TD
    %% Frontend Layer
    subgraph "Frontend Layer"
        U("Frontend UI (Svelte/TypeScript/Tailwind)") 
    end

    %% Backend Layer
    subgraph "Backend Layer"
        B("Backend API (Django/Python)")
        D("Database (SQLite)")
        B -->|"CRUD"| D
    end

    %% CLI & Shared Modules
    subgraph "CLI & Shared Modules"
        C("CLI Tool (Python)")
        S("Shared Libraries")
        T("Toolbox Utilities")
        C -->|"Uses"| S
        C -->|"Uses"| T
    end

    %% Deployment & CI/CD
    subgraph "Deployment & CI/CD"
        I("Infrastructure (Docker, DevContainers)")
        G("CI/CD & Release Scripts")
        G -->|"DeploysTo"| I
    end

    %% External Services
    A("Azure DevOps Services"):::external

    %% Interactions
    U -->|"REST/WebSocket"| B
    B -->|"Integrates"| A
    C -->|"Triggers"| A
    I -->|"Hosts"| U
    I -->|"Hosts"| B
    I -->|"Hosts"| C

    %% Click Events
    click U "https://github.com/farzammohammadi/ado-express/tree/main/ado_express_app/"
    click B "https://github.com/farzammohammadi/ado-express/tree/main/ado_express_api/"
    click C "https://github.com/farzammohammadi/ado-express/blob/main/ado_express/main.py"
    click S "https://github.com/farzammohammadi/ado-express/tree/main/ado_express/packages/shared/"
    click T "https://github.com/farzammohammadi/ado-express/tree/main/ado_express/packages/toolbox/"
    click I "https://github.com/farzammohammadi/ado-express/tree/main/.devcontainer/"
    click G "https://github.com/farzammohammadi/ado-express/tree/main/.github/workflows/"

    %% Styles
    classDef frontend fill:#D9EAD3,stroke:#6AA84F,stroke-width:2px;
    classDef backend fill:#FCE5CD,stroke:#E69138,stroke-width:2px;
    classDef cli fill:#C9DAF8,stroke:#3C78D8,stroke-width:2px;
    classDef deployment fill:#EAD1DC,stroke:#B8549E,stroke-width:2px;
    classDef external fill:#FFF2CC,stroke:#BF9000,stroke-width:2px;

    class U frontend;
    class B,D backend;
    class C,S,T cli;
    class I,G deployment;
'''