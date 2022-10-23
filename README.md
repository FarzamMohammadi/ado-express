# ADO Express

### BEFORE RUNNING - Set environment variables & deployment plan
    - The ".env" file aka environment variables file can be found in root directory
    - Deployment plan excel file can be found in files/deployment
### Update pip
    run "python -m pip install --upgrade pip"
### VS Code Development Container
    If you wish to run this app without any installations, you can do so by running your local development environment inside a container. 

    Steps:
    1. Open the project in VS Code
    2. Press F1
    3. Search for "Dev Containers: Rebuild and Reopen in Container" and press enter

    **Make sure the environment variables & deployment plan is set before running the development container
## To Run
### 1. Create virtual environment: 
    "python -m venv ./venv"
### 2. Activate VENV:
    Windows - ".\venv\Scripts\activate"
    Linux/macOS - "source venv/bin/activate"
### 3. Install Dependencies:
    "pip install -r requirements.txt"
### 4. Set "ado_express" as working directory:
    "cd ado_express"
### 5. Start app:
    "python main.py"