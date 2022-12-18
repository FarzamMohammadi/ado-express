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
            4. The latest deployed release specified by stage (*VIA_STAGE_SOURCE_NAME*) gets returned
                - Grabbing the latest release already deployed to *VIA_STAGE_SOURCE_NAME* and not yet deployed to *RELEASE_STAGE_NAME*
        - [Setps for rollback release retrieval](#getting-rollback-releases)
        
        [EXAMPLE CONFIGURATION](#search-via-query)

2. Using deployment plan excel file:
    - How does it work?
        - Iterates through release definitions found in deployment plan file to create release notes
        - Steps for target release retrieval:
            1. Goes through each release definition in the deployment plan 
            2. Finds the latest release based on last successful deployment
            3. The latest deployed release specified by stage (*VIA_STAGE_SOURCE_NAME*) gets returned
                - Grabbing the latest release already deployed to *VIA_STAGE_SOURCE_NAME* and not yet deployed to *RELEASE_STAGE_NAME*
        - [Setps for rollback release retrieval](#getting-rollback-releases)

        [EXAMPLE CONFIGURATION](#search-via-latest-release)
    
## Create Search Release Logs 
1. Search via stage in release definition:
    - How does it work? 
        - Must set release details in the deployment plan excel file
        - Goes through each release definition in deployment plan 
        - Checks the stage and deployment status of each release
        - Logs all releases in the release definition, which are successfully deployed to the stage specified by *RELEASE_STAGE_NAME*
    
    [EXAMPLE CONFIGURATION](#search-via-stageenvironment-in-release-defintions) 

2. Search via release definition and release number:
    - How does it work? 
        - Must set release details in the deployment plan excel file
        - Goes through each release definition in deployment plan
        - Finds the exact release specified by release number 
        - Logs the name and deployment status of each stages/environment for that particular release

    [EXAMPLE CONFIGURATION](#search-via-release-number-in-release-defintions)

# Deploy
There are three types of deployment available:
1. [**Deploy via query**](#deploy-via-query)
2. [**Deploy via release number**](#deploy-via-release-number)
3. [**Deploy via stage/environment**](#deploy-via-stageenvironment)

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
        4. The latest deployed release specified by stage (*VIA_STAGE_SOURCE_NAME*) gets returned
            - Grabbing the latest release already deployed to *VIA_STAGE_SOURCE_NAME* and not yet deployed to *RELEASE_STAGE_NAME*
    - [Setps for rollback release retrieval](#getting-rollback-releases)
    
    [EXAMPLE CONFIGURATION](#deploy-via-query-1)
## Deploy via release number
The use of a deployment plan file is required. The default deployment plan can be found [here](./ado_express/files/deployment). 
- How does it work? 
    - Goes through each release number in the deployment plan and deploys it to stage specified by *RELEASE_STAGE_NAME*
    - **Target Release**: Set by "Release Number" in the deployment plan (or pass as command line argument) 
    - **Target Stage/Env**: Set by *RELEASE_STAGE_NAME* environment variable (or pass as command line argument)
    - **Rollback**: Set the "Rollback Number" in the deployment plan file (or pass as command line argument)
    
    [EXAMPLE CONFIGURATION](#deploy-via-release-number-1)

## Deploy via stage/environment
The use of a deployment plan file is required. The default deployment plan can be found [here](./ado_express/files/deployment). 
- How does it work?
    - Goes through each release definition in the deployment plan. Then finds and deploys latest release based on RELEASE_STAGE_NAME.
    - **Target**: Found by going through all the releases in release definition. Then selecting the last release successfully deployed to stage specified by *VIA_STAGE_SOURCE_NAME*
    - **Rollback**: Found by going through all the releases in release definition. Then selecting the last release successfully deployed to stage specified by *RELEASE_STAGE_NAME*

    [EXAMPLE CONFIGURATION](#deploy-via-stageenvironment-1)

# Getting Rollback Releases
Finds the last deployed release in target stage and sets it as rollback. **Query** and **via_latest** features use this method for getting rollback releases.

- How does it work?
    - Iterates through release definitions found in the release target retrieval step
    - Checks the stage and deployment status of each
    - Returns the latest deployed release that matches stage specified by *RELEASE_STAGE_NAME*
        - In other words, the last release in the release definition deployed to *RELEASE_STAGE_NAME*

---------------------------------
# Ways to run
- [**Executable** (No installation required)](#1-executable-simplest-method---no-installation-required)
- [**Locally in development container** (Docker & VSCode installation required - Python & dependency installation not required)](#2-locally-in-development-container-docker--vscode-installation-required)
- [**Locally** (python & dependency installation required)](#3-locally-python--dependency-installation-required)

## 1. Executable (Simplest method - No installation required)
Executables for Windows and Linux are available in repository release artifacts. Download and run the executable file with the desired parameters. 

    ado-express-{OS}.exe <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE>

#### Environment Variables Configuration
Pass the environment variables as parameters in command. More about environment variables here: [Environment Variables](#Environment-Variables):

## 2. Locally in Development Container (Docker & VSCode installation required)
You can run or contribute to this project without installing python or other project dependencies. You can do this by running your local development environment inside a container. For more info: (https://code.visualstudio.com/docs/devcontainers/containers)

Steps:
1. Open the project in VS Code
2. Press F1
3. Search for "Dev Containers: Rebuild and Reopen in Container" and press enter (Docker must be running)

**IMPORTANT: The start of a development container, will trigger the application to run. To prevent this, don't setup the environment variables. You can always set them after the development container has started.**

### To run the application within the development container

Using environment variables in .env:
    
    python ado_express/main.py

Using command line arguments:
    
    python ado_express/main.py <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE>

#### Environment Variables Configuration
There are two ways to set the environment variables:
1. Set them in .env file
2. Pass them as arguments in the run command

Make sure to set them according to your task via either the run command or .env file. For more information about environment variables, see [Environment Variables](#Environment-Variables).
## 3. Locally (Python & Dependency Installation Required)

### Python & pip installation
Must have python (https://www.python.org/downloads/) and pip (https://www.activestate.com/resources/quick-reads/how-to-install-pip-on-windows/) installed. Then run the command below to update pip:
    
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
    
    python ado_express/main.py <CRUCIAL_RELEASE_DEFINITIONS> <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE>

#### Environment Variables Configuration
There are two ways to set the environment variables:
1. Set them in .env file
2. Pass them as arguments in the run command

Make sure to set them according to your task via either the run command or .env file. For more information about environment variables, see [Environment Variables](#Environment-Variables).

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
Note: The default values of these variables are null and false

- **CRUCIAL_RELEASE_DEFINITIONS**=< Array of release definitions that are crucial to the deployment process - Example: releaseone,releasetwo,releasethree >
- **ORGANIZATION_URL**=< Your organizations ADO URL - Example: https://dev.azure.com/{organization} >
- **PERSONAL_ACCESS_TOKEN**=< Personal access token (https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows) >
- **QUERY**=< ID of ADO query containing work items to retrieve releases from (ID must be from a saved query and cannot be from a temporary query) >
- **RELEASE_STAGE_NAME**=< Name of the stage you wish to deploy your releases to (Target)- Example: PROD >
- **RELEASE_NAME_FORMAT**=< Release name format - Example: Release-$(rev:r) >
- **SEARCH_ONLY**=< true/false >
- **VIA_STAGE**=< true/false >
- **VIA_STAGE_SOURCE_NAME**=< Name of the stage that has releases successfully deployed to it already (Rollback) - Example: QA >
- **VIA_STAGE_LATEST_RELEASE**=< true/false >

### Order of Command Line Arguments
    <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE> <CRUCIAL_RELEASE_DEFINITIONS>

**Based on your format, you may need to set *RELEASE_NAME_FORMAT* in quotation marks**

# Configuration Examples
While I continue to work on making the use of this tool easier, it could be confusing at first to know how to set the environment variables. Here are examples of each run setting environment variables to help with the use of this tool:

## Search
### Search via query
.env:

    PERSONAL_ACCESS_TOKEN=tokenxxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    SEARCH_ONLY=True
    VIA_STAGE=True
    VIA_STAGE_SOURCE_NAME=QA
    QUERY=queryID/queryURL

CMD:

    ./ado-express-linux.exe None https://dev.azure.com/xxxx tokenxxxx queryURL PROD "Release-$(rev:r)" True True QA
**Set *RELEASE_NAME_FORMAT* in quotations**

### Search via latest release
    PERSONAL_ACCESS_TOKEN=xxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    VIA_STAGE=True
    VIA_STAGE_LATEST_RELEASE=True
    VIA_STAGE_SOURCE_NAME=QA
    SEARCH_ONLY=True

### Search via stage/environment in release defintions
    PERSONAL_ACCESS_TOKEN=xxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    VIA_STAGE=True
    SEARCH_ONLY=True

### Search via release number in release defintions
    PERSONAL_ACCESS_TOKEN=xxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    SEARCH_ONLY=True

## Deploy

### Deploy via query
.env:

    PERSONAL_ACCESS_TOKEN=tokenxxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    VIA_STAGE=True
    VIA_STAGE_SOURCE_NAME=QA
    QUERY=queryID/queryURL

CMD:

    ./ado-express-linux.exe None https://dev.azure.com/xxxx tokenxxxx queryID PROD "Release-$(rev:r)" False True QA
**Set *RELEASE_NAME_FORMAT* in quotations**
### Deploy via release number
    CRUCIAL_RELEASE_DEFINITIONS=realeaseX,releaseY,releaseZ
    PERSONAL_ACCESS_TOKEN=tokenxxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers

CMD:

    ./ado-express-win.exe realeaseX,releaseY,releaseZ https://dev.azure.com/xxxx token None PROD "Release-$(rev:r)" False False None False

**Set *RELEASE_NAME_FORMAT* in quotation marks**
### Deploy via stage/environment
    PERSONAL_ACCESS_TOKEN=token
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    VIA_STAGE=True
    VIA_STAGE_SOURCE_NAME=QA

----------------------------------

# Contribution, Issues & New Features
You are more than welcome to contribute to this project by sharing your work through a pull request. If you face any issues or would like to request for any features or changes, let me know by creating a new issue here: [ADO-Express Issues](https://github.com/FarzamMohammadi/ado-express/issues)