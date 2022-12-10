# ADO Express
An Azure Devops release management tool. Able to create release notes using various methods and deploy releases - all in the most automated way possible. Tired of creating release notes? Or wasting time by manually deploying and monitoring releases? So was I, and here is my solution. Enjoy!

# Search (Create release notes or just search existing releases)
There are a total of four ways to search for releases, two of which create an excel file in the "ado_express/files/search-results" directory and output the results there, making it available for later use (e.g. deploying them after search is complete). The other two methods only log the search results and while they could prove useful, their primary purpose is for searching exsting releases.

Search and output results to excel file:
* Using ADO query ID:
    - Must provide a query ID from a saved ADO query. 
    - The tool will iterate through all of the work items in query and output the latest release target based on your environment variables. 
    - The target release will be determined using the stage provided in VIA_STAGE_SOURCE_NAME variable/argument. It will return the release target based on the latest release in the stage specified.
    - The rollback release will determined using the stage provided in RELEASE_STAGE_NAME variable/argument. It will return the release rollback, based on the latest successful deployment of the release in the stage specified. In other words, rollback will be the last successful release in target stage specified. In the case of crucial deployment error, the tool can prevent deplyoment issues by rolling back the release to the previously successful release.
* Using deployment-plan excel file:
    - Provide deployment project and definition names in deployment/deployment-plan.xlsx file
    - The target release will be determined using the stage provided in VIA_STAGE_SOURCE_NAME variable/argument. It will return the release target based on the latest release in the stage specified.
    - The rollback release will determined using the stage provided in RELEASE_STAGE_NAME variable/argument. It will return the release rollback, based on the latest successful deployment of the release in the stage specified. In other words, rollback will be the last successful release in target stage specified. In the case of crucial deployment error, the tool can prevent deplyoment issues by rolling back the release to the previously successful release.

Search and only log search results:
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

