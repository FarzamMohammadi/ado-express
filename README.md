# ADO Express
**Azure DevOps Release Management Tool**

Create release notes, search, and deploy releases - all in the most automated way possible. 

Benefits:
- Save time managing release deployments
- Achieve release uniformity in all environment deployments
- Prevent inclusion/exclusion of unwanted releases in deployments
- Automate your CD from start to end 

Enjoy!

----------------------------------
# Search
There are two types of searches available:
1. [**Export the results (to an excel file & logs)**](#create-search-release-notes-export-search-results-to-excel-file)
2. [**Log the results**](#create-search-release-logs)

## Create Search Release Notes (Export search results to excel file)
1. Using ADO query ID:
    - How does it work?
        - Iterates through work items (regardless of type) in query to find the last release created by builds of merged commits
        - Steps for target release retrieval: 
            1. Gets each work item in query
            2. Goes through each work item to get merged commit builds from pull requests and pushes
            3. Gets all releases created by builds and compares them to find the latest 
            4. The latest deployed release specified by environment (*VIA_ENV_SOURCE_NAME*) gets returned
                - Grabbing the latest release already deployed to *VIA_ENV_SOURCE_NAME* and not yet deployed to *RELEASE_TARGET_ENV*
        - [Setps for rollback release retrieval](#getting-rollback-releases)
        
        [EXAMPLE CONFIGURATION](#search-via-query)

2. Using deployment plan excel file:
    - How does it work?
        - Iterates through release definitions found in deployment plan file to create release notes
        - Steps for target release retrieval:
            1. Goes through each release definition in the deployment plan 
            2. Finds the latest release based on last successful deployment
            3. The latest deployed release specified by environment (*VIA_ENV_SOURCE_NAME*) gets returned
                - Grabbing the latest release already deployed to *VIA_ENV_SOURCE_NAME* and not yet deployed to *RELEASE_TARGET_ENV*
        - [Setps for rollback release retrieval](#getting-rollback-releases)

        [EXAMPLE CONFIGURATION](#search-via-latest-release)
    
## Create Search Release Logs 
1. Search via environment in release definition:
    - How does it work? 
        - Must set release details in the deployment plan excel file
        - Goes through each release definition in deployment plan 
        - Checks the environment and deployment status of each release
        - Logs all releases in the release definition, which are successfully deployed to the environment specified by *RELEASE_TARGET_ENV*
    
    [EXAMPLE CONFIGURATION](#search-via-environment-in-release-defintions) 

2. Search via release definition and release number:
    - How does it work? 
        - Must set release details in the deployment plan excel file
        - Goes through each release definition in deployment plan
        - Finds the exact release specified by release number 
        - Logs the name and deployment status of each environments for that particular release

    [EXAMPLE CONFIGURATION](#search-via-release-number-in-release-defintions)

# Deploy
There are three types of deployment available:
1. [**Deploy via query**](#deploy-via-query)
2. [**Deploy via release number**](#deploy-via-release-number)
3. [**Deploy via environment**](#deploy-via-environment)

**If deployment of some release definitions are crucial**: 
- Same process for all three deployment methods
- Set the "Crucial" value to True in the deployment plan file (or pass as *CRUCIAL_RELEASE_DEFINITIONS* in command line argument or as environment variable). See [List of Variables/Arguments](#list-of-variablesarguments) for more information
- In cases of deployments where the deployment plan is used, first the deployment plan file is checked for crucial release definitions via the "Crucial" column value, if nothing is found, then the *CRUCIAL_RELEASE_DEFINITIONS* is checked
- These deployments will run first in parallel
- After successfully completion, the rest of the deployments run in parallel
- In case of a crucial deployment error:
    - The application will attempt to rollback (deploy to rollback number) 
    - Then will stop the processes regardless of the status of rollback

## Deploy via query
- How does it work?
    - Iterates through work items (regardless of type) in query to find the last release created by builds of merged commits
    - Steps for target release retrieval: 
        1. Gets each work item in query
        2. Goes through each work item to get merged commit builds from pull requests and pushes
        3. Gets all releases created by builds and compares them to find the latest 
        4. The latest deployed release specified by environment (*VIA_ENV_SOURCE_NAME*) gets returned
            - Grabbing the latest release already deployed to *VIA_ENV_SOURCE_NAME* and not yet deployed to *RELEASE_TARGET_ENV*
    - [Setps for rollback release retrieval](#getting-rollback-releases)
    
    [EXAMPLE CONFIGURATION](#deploy-via-query-1)
## Deploy via release number
The use of a deployment plan file is required. The default deployment plan can be found [here](./ado_express/files/deployment). 
- How does it work? 
    - Goes through each release number in the deployment plan and deploys it to environment specified by *RELEASE_TARGET_ENV*
    - **Target Release**: Set by "Release Number" in the deployment plan (or pass as command line argument) 
    - **Target Environment**: Set by *RELEASE_TARGET_ENV* environment variable (or pass as command line argument)
    - **Rollback**: Set the "Rollback Number" in the deployment plan file (or pass as command line argument)
    
    [EXAMPLE CONFIGURATION](#deploy-via-release-number-1)

## Deploy via environment
The use of a deployment plan file is required. The default deployment plan can be found [here](./ado_express/files/deployment). 
- How does it work?
    - Goes through each release definition in the deployment plan. Then finds and deploys latest release based on RELEASE_TARGET_ENV.
    - **Target**: Found by going through all the releases in release definition. Then selecting the last release successfully deployed to environment specified by *VIA_ENV_SOURCE_NAME*
    - **Rollback**: Found by going through all the releases in release definition. Then selecting the last release successfully deployed to environment specified by *RELEASE_TARGET_ENV*

    [EXAMPLE CONFIGURATION](#deploy-via-environment-1)

# Getting Rollback Releases
Finds the last deployed release in target environment and sets it as rollback. **Query** and **via_latest** features use this method for getting rollback releases.

- How does it work?
    - Iterates through release definitions found in the release target retrieval step
    - Checks the environment and deployment status of each
    - Returns the latest deployed release that matches environment specified by *RELEASE_TARGET_ENV*
        - In other words, the last release in the release definition deployed to *RELEASE_TARGET_ENV*

---------------------------------
# Ways to run
- [**Docker**](#1-docker)
- [**Executable** (No installation required)](#2-executable-simplest-method---no-installation-required)
- [**Locally in development container** (Docker & VSCode installation required - Python & dependency installation not required)](#3-locally-in-development-container-docker--vscode-installation-required)
- [**Locally** (python & dependency installation required)](#4-locally-python--dependency-installation-required)

## 1. Docker
You can pull the latest image directly from the [packeges](https://github.com/FarzamMohammadi/ado-express/pkgs/container/ado-express) section of this repo.

## 2. Executable (Simplest method - No installation required)
Executables for Windows and Linux are available in repository release artifacts. Download and run the executable file with the desired parameters. 

    ado-express-{OS}.exe <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_NAME_FORMAT> <RELEASE_TARGET_ENV> <SEARCH_ONLY> <VIA_ENV> <VIA_ENV_SOURCE_NAME> <VIA_ENV_LATEST_RELEASE>

#### Environment Variables Configuration
There are two ways to set the environment variables:
1. Pass them as arguments in the run command
2. Set them in the environment

Make sure to set them according to your task. For more information about environment variables, see [Environment Variables](#Environment-Variables).

## 3. Locally in Development Container (Docker & VSCode installation required)
You can run or contribute to this project without installing python or other project dependencies. You can do this by running your local development environment inside a container. For more info, see [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers).

Steps:
1. Open the project in VS Code
2. Press F1
3. Search for "Dev Containers: Rebuild and Reopen in Container" and press enter (Docker must be running)

**IMPORTANT: The start of a development container, will trigger the application to run. To prevent this, don't setup the environment variables. You can always set them after the development container has started.**

### To run the application within the development container

Using environment variables in .env:
    
    python ado_express/main.py

Using command line arguments:
    
    python ado_express/main.py <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_NAME_FORMAT> <RELEASE_TARGET_ENV> <SEARCH_ONLY> <VIA_ENV> <VIA_ENV_SOURCE_NAME> <VIA_ENV_LATEST_RELEASE>

#### Environment Variables Configuration
There are three ways to set the environment variables:
1. Set them in .env file
2. Pass them as arguments in the run command
3. Set them in the environment

Make sure to set them according to your task. For more information about environment variables, see [Environment Variables](#Environment-Variables).
## 4. Locally (Python & Dependency Installation Required)

### Python & pip installation
Must have [Python](https://www.python.org/downloads/) and [pip](https://www.activestate.com/resources/quick-reads/how-to-install-pip-on-windows/) installed. Then run the command below to update pip:
    
    python -m pip install --upgrade pip

### Run application
#### 1. Create virtual environment
    python -m venv ./venv
#### 2. Activate VENV
    Windows - .\venv\Scripts\activate
    Linux/macOS - source venv/bin/activate
#### 3. Install Dependencies
    pip install -r requirements.txt
#### 4. Run application
Using environment variables in .env:
    
    python ado_express/main.py

Using command line arguments:
    
    python ado_express/main.py <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_NAME_FORMAT> <RELEASE_TARGET_ENV> <SEARCH_ONLY> <VIA_ENV> <VIA_ENV_SOURCE_NAME> <VIA_ENV_LATEST_RELEASE>

#### Environment Variables Configuration
There are three ways to set the environment variables:
1. Set them in .env file
2. Pass them as arguments in the run command
3. Set them in the environment

Make sure to set them according to your task. For more information about environment variables, see [Environment Variables](#Environment-Variables).

---------------------------------
# Files & Resources
All the files and resources can be found under the [files directory](./ado_express/files).

## [/deployment](./ado_express/files/deployment)
- *deployment-plan.xlsx*: Deployment plan file used by default for search and deployment

## [/logs](./ado_express/files/logs)
- *deployment-stale.log*: Used by development container postCreateCommand to copy contents of deployment.log
- *deployment.log*: Containts deployment logs

## [/search-results](./ado_express/files/search-results)
- *deployment-plan.xlsx*: The output of search results
- *search-results.log*: Contains search logs
# Environment Variables
## List of Variables/Arguments
Note: The default values of these variables are none/null and false

- **CRUCIAL_RELEASE_DEFINITIONS**=< Array of release definitions that are crucial to the deployment process - Example: releaseone,releasetwo,releasethree >
- **ORGANIZATION_URL**=< Your organizations ADO URL - Example: https://dev.azure.com/{organization} >
- **PERSONAL_ACCESS_TOKEN**=< Personal access token (https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows) >
- **QUERY**=< ID of ADO query containing work items to retrieve releases from (ID must be from a saved query and cannot be from a temporary query) >
- **RELEASE_NAME_FORMAT**=< Release name format - Example: Release-$(rev:r) >
- **RELEASE_TARGET_ENV**=< Name of the environment you wish to deploy your releases to (Target)- Example: PROD >
- **SEARCH_ONLY**=< true/false >
- **VIA_ENV**=< true/false >
- **VIA_ENV_SOURCE_NAME**=< Name of the environment that has releases successfully deployed to it already (Rollback) - Example: QA >
- **VIA_ENV_LATEST_RELEASE**=< true/false >

### Order of Command Line Arguments
    <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_NAME_FORMAT> <RELEASE_TARGET_ENV> <SEARCH_ONLY> <VIA_ENV> <VIA_ENV_SOURCE_NAME> <VIA_ENV_LATEST_RELEASE>

**Based on your format, you may need to set *RELEASE_NAME_FORMAT* in quotation marks**

# Configuration Examples
While I continue to work on making the use of this tool easier, it could be confusing at first to know how to set the environment variables. Here are examples of each run setting environment variables to help with the use of this tool:

## Search
### Search via query
Required: ORGANIZATION_URL, PERSONAL_ACCESS_TOKEN, RELEASE_NAME_FORMAT, RELEASE_TARGET_ENV, SEARCH_ONLY, VIA_ENV, VIA_ENV_SOURCE_NAME, QUERY

.env:

    ORGANIZATION_URL=https://dev.azure.com/xxxx
    PERSONAL_ACCESS_TOKEN=tokenxxxx
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    RELEASE_TARGET_ENV=PROD
    SEARCH_ONLY=True
    VIA_ENV=True
    VIA_ENV_SOURCE_NAME=QA
    QUERY=queryID/queryURL

CMD:

    ./ado-express-linux.exe None https://dev.azure.com/xxxx tokenxxxx queryURL "Release-$(rev:r)" PROD True True QA
**Set *RELEASE_NAME_FORMAT* in quotations**

### Search via latest release
Required: ORGANIZATION_URL, PERSONAL_ACCESS_TOKEN, RELEASE_NAME_FORMAT, RELEASE_TARGET_ENV, SEARCH_ONLY, VIA_ENV, VIA_ENV_LATEST_RELEASE, VIA_ENV_SOURCE_NAME

.env:

    ORGANIZATION_URL=https://dev.azure.com/xxxx
    PERSONAL_ACCESS_TOKEN=xxxx
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    RELEASE_TARGET_ENV=PROD
    SEARCH_ONLY=True
    VIA_ENV=True
    VIA_ENV_LATEST_RELEASE=True
    VIA_ENV_SOURCE_NAME=QA

### Search via environment in release defintions
Required: ORGANIZATION_URL, PERSONAL_ACCESS_TOKEN, RELEASE_NAME_FORMAT, RELEASE_TARGET_ENV, SEARCH_ONLY, VIA_ENV

.env:

    ORGANIZATION_URL=https://dev.azure.com/xxxx
    PERSONAL_ACCESS_TOKEN=xxxx
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    RELEASE_TARGET_ENV=PROD
    SEARCH_ONLY=True
    VIA_ENV=True

### Search via release number in release defintions
Required: ORGANIZATION_URL, PERSONAL_ACCESS_TOKEN, RELEASE_NAME_FORMAT, SEARCH_ONLY

.env:

    ORGANIZATION_URL=https://dev.azure.com/xxxx
    PERSONAL_ACCESS_TOKEN=xxxx
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    SEARCH_ONLY=True

## Deploy

### Deploy via query
Required: ORGANIZATION_URL, PERSONAL_ACCESS_TOKEN, RELEASE_NAME_FORMAT, RELEASE_TARGET_ENV, VIA_ENV, VIA_ENV_SOURCE_NAME, QUERY

.env:
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    PERSONAL_ACCESS_TOKEN=tokenxxxx
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    RELEASE_TARGET_ENV=PROD
    VIA_ENV=True
    VIA_ENV_SOURCE_NAME=QA
    QUERY=queryID/queryURL

CMD:

    ./ado-express-linux.exe None https://dev.azure.com/xxxx tokenxxxx queryID "Release-$(rev:r)" PROD False True QA
**Set *RELEASE_NAME_FORMAT* in quotations**
### Deploy via release number
Required: ORGANIZATION_URL, PERSONAL_ACCESS_TOKEN, RELEASE_NAME_FORMAT, RELEASE_TARGET_ENV

.env:

    CRUCIAL_RELEASE_DEFINITIONS=realeaseX,releaseY,releaseZ
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    PERSONAL_ACCESS_TOKEN=tokenxxxx
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    RELEASE_TARGET_ENV=PROD

CMD:

    ./ado-express-win.exe realeaseX,releaseY,releaseZ https://dev.azure.com/xxxx token None "Release-$(rev:r)" PROD False False None False

**Set *RELEASE_NAME_FORMAT* in quotation marks**
### Deploy via environment
Required: ORGANIZATION_URL, PERSONAL_ACCESS_TOKEN, RELEASE_NAME_FORMAT, RELEASE_TARGET_ENV, VIA_ENV, VIA_ENV_SOURCE_NAME

.env:

    ORGANIZATION_URL=https://dev.azure.com/xxxx
    PERSONAL_ACCESS_TOKEN=token
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    RELEASE_TARGET_ENV=PROD
    VIA_ENV=True
    VIA_ENV_SOURCE_NAME=QA

----------------------------------

# Contribution, Issues & New Features
You are more than welcome to contribute to this project by sharing your work through a pull request. If you face any issues or would like to request for any features or changes, let me know by creating a new issue here: [ADO-Express Issues](https://github.com/FarzamMohammadi/ado-express/issues)