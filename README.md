# ADO Express
**Azure Devops release management tool**

Able to create release notes using various methods and deploy releases - all in the most automated way possible. Tired of creating release notes? Or wasting time by manually deploying and monitoring releases? So was I, and here is my solution. Enjoy!

# Search
There are two types of search available:
1. [**Export the results to an excel file** (Can be used later for deployment)](#create-search-release-notes-export-search-results-to-excel-file)
2. [**Log the results**](#create-search-release-logs)

## Create Search Release Notes (Export search results to excel file)
- Using ADO query ID:
    - How does it work?
        - This search method will use all the work items (regardless of type) in your query to create release notes by retrieving the latest releases created in the said work item builds.  
        - Getting Target Releases: It will do this by going though all the builds created via pull requests and pushes to the repositroy. After gettings all the work item builds, it will then go thorugh each release created by each build and return the latest one for that release definition based on the releases that have successfully been deployed to the stage set by the VIA_STAGE_SOURCE_NAME environment variable. This will then become the target release for each release definition found.

        [EXAMPLE CONFIGURATION](#search-by-query)

- Using deployment plan excel file:
    - How does it work?
        - This search method will use all the release definitions found in the deployment plan excel file to create release notes.
        - Getting Target Releases: It will do this by going thorugh each release definitnon in the deployment plan and finding the latest release based that all the releases that have successfully been deployed to the stage set by the VIA_STAGE_SOURCE_NAME environment variable. 

        [EXAMPLE CONFIGURATION](#search-by-latest-release)

**Getting Rollback Releases** (Same for both methods): It's retrieved by going through each release definition found in the previous step, and finding the latest release based on what is the last successfully deployed release to the RELEASE_STAGE_NAME environment variable. Essentially, setting the last successfully deployed release found for release definition as rollback. This can be used to determine what release you need to rollback your deplyoment to, in case of deployment issues.

## Create Search Release Logs 
Both methdods require using the deployment plan excel file:

1. Search by stage in release definition:
    - How does it work? 
        - Goes thorugh reach release definition in deployment plan and then finds and logs each successfully deployed release to the stage set in RELEASE_STAGE_NAME environment variable. Essentially returning all the previously deployed releases to that stage for that release definition. 
    
    [EXAMPLE CONFIGURATION](#search-by-stageenvironment-in-release-defintions) 

2. Search by release definition and release number:
    - How does it work? 
        - Goes thorugh reach release definition in deployment plan and finds the exact release specified by release number. It will then find and log the name and status of each stages/environment for that particular release. 

    [EXAMPLE CONFIGURATION](#search-by-release-number-in-release-defintions)


# Contribution & Issues
You are more than welcome to contribute to this project. You can do so, by sharing your work through a pull request. If you face any issues, let me know by creating a new issue here: [ADO-Express Issues](https://github.com/FarzamMohammadi/ado-express/issues)

---------------------------------
# Ways to run:
* Use executable (No installation required)
* Use vscode development container (Docker & VSCode installation required - Python & dependency installation NOT required)
* Run the application locally (python & dependency installation required)

## 1. Use executable (Simplest method - No install required)
Executables for Windows and Linux are available in repositroy release artifacts. 

To run, download and enter the following command (make sure to set the environment variables needed for your task via the run command. For more information about environment variables, see [Environment Variables](#Environment-Variables)):

    main.exe <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE> <CRUCIAL_RELEASE_DEFINITIONS> <USE_SEARCH_RESULTS>

## 2. Use VSCode Development Container (Docker & VSCode installation required)
If you wish to run or contribute to this app without any dependecy installations, you can do so by running your local development environment inside a container (https://code.visualstudio.com/docs/devcontainers/containers). Keep in mind that docker and vscode installation is required.

Steps:
1. Open the project in VS Code
2. Press F1
3. Search for "Dev Containers: Rebuild and Reopen in Container" and press enter (Docker must be running)

**IMPORTANT: If the environment variables and deployment plan (in deployment or search-results directory) are set before running the development container then the start of the development will trigger an actual run (meaning it could possbile deploy your releases). To prevent this, simply don't setup the environment variables. You can always set them after the develeopment container has started.**

## To run the application within the development container:
#### Environment Variables Configuration
There are 2 ways to set the environment variables:
* Set them in .env file
* Pass them as arguments in the run command (Must remove example values from .env files) 

Make sure to set them according to your task via either the run command or .env file. For more information about environment variables, see [Environment Variables](#Environment-Variables)). Once you have set the environment variables, run one of the following commands based on your environment variable configuration:

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
### 4. Set "ado_express" as working directory:
    cd ado_express
### 5. Start app:
#### Environment Variables Configuration
There are 2 ways to set the environment variables:
* Set them in .env file
* Pass them as arguments in the run command (Must remove example values from .env files) 

Make sure to set them according to your task via either the run command or .env file. For more information about environment variables, see [Environment Variables](#Environment-Variables)). Once you have set the environment variables, run one of the following commands based on your environment variable configuration:

Using environment variables in .env:
    
    python ado_express/main.py

Using command line arguments:
    
    python ado_express/main.py <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE> <CRUCIAL_RELEASE_DEFINITIONS> <USE_SEARCH_RESULTS>


---------------------------------
Additional Information About the Project
# Files & Resources
All the files and resources can be found under the [files directory](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files).

## [/deployment](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files/deployment)
* *deployment-plan.xlsx*: Deployment plan file used by default for search and deployment

## [/logs](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files/logs)
* *deployment-stale.log*: Used by development container postCreateCommand to copy contents of deployment.log to it
* *deployment.log*: Containts deployment logs

## [/search-results](https://github.com/FarzamMohammadi/ado-express/tree/main/ado_express/files/search-results)
* *deployment-plan.xlsx*: The output of search results that results in release note creation. This can also by used for deployment if USE_SEARCH_RESULTS environment variable is set to true
* *search-results.log*: Contains search logs
# Environment Variables
### Considerations:
1. The default values of these variables are null and false
2. You must remove the .env example values to use command line arguments

## List of Variables/Arguments

* **ORGANIZATION_URL**=< Your organizations ADO URL - Example: https://dev.azure.com/{organization} >
* **PERSONAL_ACCESS_TOKEN**=< Personal access token (https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows) >
* **QUERY**=< ID of ADO query containing work items to retrieve releases from (ID must be from a saved query and cannot be from a temporary query) >
* **RELEASE_STAGE_NAME**=< Name of the stage you wish to deploy your releases to (Target)- Example: PROD >
* **RELEASE_NAME_FORMAT**=< Release name format - Example: Release-$(rev:r) >
* **SEARCH_ONLY**=< true/false >
* **VIA_STAGE**=< true/false >
* **VIA_STAGE_SOURCE_NAME**=< Name of the stage that has releases successfully deployed to it already (Rollback) - Example: QA >
* **VIA_STAGE_LATEST_RELEASE**=< true/false >
* **CRUCIAL_RELEASE_DEFINITIONS**=< Array of release definitions that are crucial to the deployment process - Example: releaseone,releasetwo,releasethree >
* **USE_SEARCH_RESULTS**=< true/false - Will use deploymeny-plan.xlsx in search-results directory instead of default deployment plan in deployment directory >

### Order of Command Line Arguments
    <ORGANIZATION_URL> <PERSONAL_ACCESS_TOKEN> <QUERY> <RELEASE_STAGE_NAME> <RELEASE_NAME_FORMAT> <SEARCH_ONLY> <VIA_STAGE> <VIA_STAGE_SOURCE_NAME> <VIA_STAGE_LATEST_RELEASE> <CRUCIAL_RELEASE_DEFINITIONS> <USE_SEARCH_RESULTS>

While I am intent on making the use of this tool easier, it could be confusing at first to know how to set the environment variables. Here are various examples of pre-setup .env variables to help with the use of this tool:

## Search by query: 
    PERSONAL_ACCESS_TOKEN=xxxx
    ORGANIZATION_URL=https://dev.azure.com/xxxx
    RELEASE_STAGE_NAME=PROD
    RELEASE_NAME_FORMAT=Release-$(rev:r) <- '$' will be used to split the release names and numbers
    SEARCH_ONLY=True
    VIA_STAGE=True
    VIA_STAGE_SOURCE_NAME=QA
    QUERY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

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