# ADO Express
**Azure DevOps Release Management Tool**

Search, create release notes and deploy releases - all in the most automated way possible. Tired of creating release notes? Or wasting time by manually deploying and monitoring the status of releases? So was I, and here is my solution. Enjoy!

----------------------------------

- [Search](#search)
    - [Export the results to an excel file](#create-search-release-notes-export-search-results-to-excel-file)
    - [Log the results](#create-search-release-logs)
- [Deploy](#deploy)
    - [Deploy via release number](#deploy-via-release-number)
	- [Deploy via stage/environment](#deploy-via-stageenvironment)
- [Ways to run](#ways-to-run)
    - [Use executable](#1-use-executable-simplest-method---no-install-required)
    - [Use VSCode Development Container](#2-use-vscode-development-container-docker--vscode-installation-required)
    - [Run the application locally](#3-run-the-application-locally-python--dependency-installation-required)
- [Files & Resources](#files--resources)
- [Environment Variables](#environment-variables)
    - [List of Variables/Arguments](#list-of-variablesarguments)
- [Configuration Examples](#configuration-cxamples)
- [Contribution, Issues & New Features](#contribution-issues--new-features)

----------------------------------

# Search
There are two types of searches available:
1. [**Export the results to an excel file** (Can be used later for deployment)](#create-search-release-notes-export-search-results-to-excel-file)
2. [**Log the results**](#create-search-release-logs)

## Create Search Release Notes (Export search results to excel file)
### 2 Ways to run:
- Using ADO query ID:
    - How does it work?
        - Iterates through work items (regardless of type) in query to find the last release created by builds of merged commits
        - Steps for target release retrieval: 
            1. Gets each work item in query
            2. Goes through each work item to get merged commit builds from pull requests and pushes
            3. Gets all releases created by builds and compares them to find the latest 
            4. The latest deployed release specified by stage (*VIA_STAGE_SOURCE_NAME*) gets returned
        - [Setps for rollback release retrieval](#getting-rollback-releases-same-for-both-methods)
        
        [EXAMPLE CONFIGURATION](#search-by-query)

- Using deployment plan excel file:
    - How does it work?
        - Iterates through release definitions found in deployment plan file to create release notes
        - Steps for target release retrieval:
            1. Goes through each release definition in the deployment plan 
            2. Finds the latest release based on last successful deployment
            3. The latest deployed release specified by stage (*VIA_STAGE_SOURCE_NAME*) gets returned
        - [Setps for rollback release retrieval](#getting-rollback-releases-same-for-both-methods)

        [EXAMPLE CONFIGURATION](#search-by-latest-release)

### Getting Rollback Releases (Same for both methods): 
Finds the last deployed release in target stage and sets it as rollback.
- Steps:
    1. Iterates through release definitions found in the release target retrieval step
    2. Checks the stage and deployment status of each
    3. Returns the latest deployed release that matches stage specified by *RELEASE_STAGE_NAME*
    
## Create Search Release Logs 
Both methods need using the deployment plan excel file:

1. Search by stage in release definition:
    - How does it work? 
        - Goes through each release definition in deployment plan 
        - Checks the stage and deployment status of each release
        - Logs releases successfully deployed to stage specified by *RELEASE_STAGE_NAME*
    
    [EXAMPLE CONFIGURATION](#search-by-stageenvironment-in-release-defintions) 

2. Search by release definition and release number:
    - How does it work? 
        - Goes through each release definition in deployment plan
        - Finds the exact release specified by release number 
        - Log the name and deployment status of each stages/environment for release

    [EXAMPLE CONFIGURATION](#search-by-release-number-in-release-defintions)

# Deploy
The use of a deployment plan file is required. The default deployment plan can be found [here](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files/deployment). You can use the search results deployment plan (found [here](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files/search-results)), by setting *USE_SEARCH_RESULTS* to true. There are two types of deployment available:
1. [**Deploy via release number**](#deploy-via-release-number)
2. [**Deploy via stage/environment**](#deploy-via-stageenvironment)

**If deployment is crucial (Same configuration for both deployment methods)**: 
- Set the "Crucial" value to True in the deployment plan file (or pass as *CRUCIAL_RELEASE_DEFINITIONS*)
- These deployments will run first in parallel
- After successfully completion the rest of the deployments run in parallel
- In case of a crucial deployment error:
    - The application will attempt to rollback (deploy to rollback number) 
    - Then will stop the processes regardless of the status of rollback

## Deploy via release number
- How does it work? 
    - Goes through each release number in the deployment plan and deploys it to stage specified by *RELEASE_STAGE_NAME*
    - **Target Release**: Set by "Release Number" in the deployment plan (or pass as command line argument) 
    - **Target Stage/Env**: Set by *RELEASE_STAGE_NAME* environment variable (or pass as command line argument)
    - **Rollback**: Set the "Rollback Number" in the deployment plan file (or pass as command line argument)
    
    [EXAMPLE CONFIGURATION](#deploy-via-release-number-1)

## Deploy via stage/environment
- How does it work?
    - Goes through each release definition in the deployment plan. Then finds and deploys latest release based on RELEASE_STAGE_NAME.
    - **Target**: Found by going through all the releases in release definition. Then selecting the last release successfully deployed to stage specified by *VIA_STAGE_SOURCE_NAME*
    - **Rollback**: Found by going through all the releases in release definition. Then selecting the last release successfully deployed to stage specified by *RELEASE_STAGE_NAME*

    [EXAMPLE CONFIGURATION](#deploy-via-stageenvironment-1)

---------------------------------
# Ways to run
- [**Use executable** (No installation required)](#1-use-executable-simplest-method---no-install-required)
- [**Use vscode development container** (Docker & VSCode installation required - Python & dependency installation not required)](#2-use-vscode-development-container-docker--vscode-installation-required)
- [**Run the application locally** (python & dependency installation required)](#3-run-the-application-locally-python--dependency-installation-required)

## 1. Use executable (Simplest method - No install required)
Executables for Windows and Linux are available in repository release artifacts. 

To run, download and enter the following command (pass the environment variables as parameters in command). For more information about environment variables, see [Environment Variables](#Environment-Variables)):

    ado-express-{OS}.exe <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE> <CRUCIAL_RELEASE_DEFINITIONS> <USE_SEARCH_RESULTS>

## 2. Use VSCode Development Container (Docker & VSCode installation required)
You can run or contribute to this project without installing python or other project dependencies. You can do this by running your local development environment inside a container (https://code.visualstudio.com/docs/devcontainers/containers).

Steps:
1. Open the project in VS Code
2. Press F1
3. Search for "Dev Containers: Rebuild and Reopen in Container" and press enter (Docker must be running)

**IMPORTANT: The start of a development container, will trigger the application to run. To prevent this, don't setup the environment variables. You can always set them after the development container has started.**
## To run the application within the development container:
#### Environment Variables Configuration
There are two ways to set the environment variables:
1. Set them in .env file
2. Pass them as arguments in the run command (Must remove example values from .env files) 

Make sure to set them according to your task via either the run command or .env file. For more information about environment variables, see [Environment Variables](#Environment-Variables)).

Using environment variables in .env:
    
    python ado_express/main.py

Using command line arguments:
    
    python ado_express/main.py <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE> <CRUCIAL_RELEASE_DEFINITIONS> <USE_SEARCH_RESULTS>
## 3. Run the application locally (Python & Dependency Installation Required)

### Python & pip installation
Must have python (https://www.python.org/downloads/) and pip (https://www.activestate.com/resources/quick-reads/how-to-install-pip-on-windows/) installed. Then run the command below to update pip:
    
    python -m pip install --upgrade pip
## To run the application:
### 1. Create virtual environment: 
    python -m venv ./venv
### 2. Activate VENV:
    Windows - .\venv\Scripts\activate
    Linux/macOS - source venv/bin/activate
### 3. Install Dependencies:
    pip install -r requirements.txt
### 4. Run application:
#### Environment Variables Configuration
There are two ways to set the environment variables:
1. Set them in .env file
2. Pass them as arguments in the run command (Must remove example values from .env files) 

Make sure to set them according to your task via either the run command or .env file. For more information about environment variables, see [Environment Variables](#Environment-Variables)).

Using environment variables in .env:
    
    python ado_express/main.py

Using command line arguments:
    
    python ado_express/main.py <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE> <CRUCIAL_RELEASE_DEFINITIONS> <USE_SEARCH_RESULTS>


---------------------------------
Additional Information About the Project
# Files & Resources
All the files and resources can be found under the [files directory](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files).

## [/deployment](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files/deployment)
- *deployment-plan.xlsx*: Deployment plan file used by default for search and deployment

## [/logs](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files/logs)
- *deployment-stale.log*: Used by development container postCreateCommand to copy contents of deployment.log
- *deployment.log*: Containts deployment logs

## [/search-results](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files/search-results)
- *deployment-plan.xlsx*: The output of search results. This can also be used for deployment if *USE_SEARCH_RESULTS* is set to true
- *search-results.log*: Contains search logs
# Environment Variables
### Considerations:
1. The default values of these variables are null and false
2. You must remove the .env example values to use command line arguments

## List of Variables/Arguments

- **ORGANIZATION_URL**=< Your organizations ADO URL - Example: https://dev.azure.com/{organization} >
- **PERSONAL_ACCESS_TOKEN**=< Personal access token (https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows) >
- **QUERY**=< ID of ADO query containing work items to retrieve releases from (ID must be from a saved query and cannot be from a temporary query) >
- **RELEASE_STAGE_NAME**=< Name of the stage you wish to deploy your releases to (Target)- Example: PROD >
- **RELEASE_NAME_FORMAT**=< Release name format - Example: Release-$(rev:r) >
- **SEARCH_ONLY**=< true/false >
- **VIA_STAGE**=< true/false >
- **VIA_STAGE_SOURCE_NAME**=< Name of the stage that has releases successfully deployed to it already (Rollback) - Example: QA >
- **VIA_STAGE_LATEST_RELEASE**=< true/false >
- **CRUCIAL_RELEASE_DEFINITIONS**=< Array of release definitions that are crucial to the deployment process - Example: releaseone,releasetwo,releasethree >
- **USE_SEARCH_RESULTS**=< true/false - Will use deploymeny-plan.xlsx in search-results directory instead of default deployment plan in deployment directory >

### Order of Command Line Arguments
    <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE> <CRUCIAL_RELEASE_DEFINITIONS> <USE_SEARCH_RESULTS>

**Based on your format, you may need to set *RELEASE_NAME_FORMAT* in quotation marks**

# Configuration Examples
While I continue to work on making the use of this tool easier, it could be confusing at first to know how to set the environment variables. Here are examples of each run setting environment variables to help with the use of this tool:

## Search by query: 
.env:

    PERSONAL_ACCESS_TOKEN=token
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    SEARCH_ONLY=True
    VIA_STAGE=True
    VIA_STAGE_SOURCE_NAME=QA
    QUERY=queryID

CMD:

    ado-express-win.exe https://dev.azure.com/xxxx token queryID PROD "Release-$(rev:r)" True True QA
**Set *RELEASE_NAME_FORMAT* in quotations**

## Search by latest release:
    PERSONAL_ACCESS_TOKEN=xxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    VIA_STAGE=True
    VIA_STAGE_LATEST_RELEASE=True
    VIA_STAGE_SOURCE_NAME=QA
    SEARCH_ONLY=True

## Search by stage/environment in release defintions:
    PERSONAL_ACCESS_TOKEN=xxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    VIA_STAGE=True
    SEARCH_ONLY=True

## Search by release number in release defintions:
    PERSONAL_ACCESS_TOKEN=xxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    SEARCH_ONLY=True

## Deploy via release number:
    PERSONAL_ACCESS_TOKEN=xxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    CRUCIAL_RELEASE_DEFINITIONS=realeaseX,releaseY,releaseZ
    USE_SEARCH_RESULTS=True

CMD:

    ado-express-win.exe https://dev.azure.com/xxxx token None PROD "Release-$(rev:r)" False True QA False None True
    
**Set *RELEASE_NAME_FORMAT* in quotation marks**
## Deploy via stage/environment:
    PERSONAL_ACCESS_TOKEN=token
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    VIA_STAGE=True
    VIA_STAGE_SOURCE_NAME=QA

----------------------------------

# Contribution, Issues & New Features
You are more than welcome to contribute to this project by sharing your work through a pull request. If you face any issues or would like to request for any features or changes, let me know by creating a new issue here: [ADO-Express Issues](https://github.com/FarzamMohammadi/ado-express/issues)