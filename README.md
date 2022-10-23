# ADO Express

## Update pip
    run "python -m pip install --upgrade pip"

## BEFORE RUNNING -> Set env variables & deployment plan 
    environment variables or ".env" file can be found in root directory
    deployment plan excel file can be found in files/deployment

## To Run
1. Create virtual environment: 
        "python -m venv ./venv"
2. Activate VENV:
        Windows - ".\venv\Scripts\activate"
        Linux/macOS - "source venv/bin/activate"
3. Install Dependencies:
        "pip install -r requirements.txt"
4. Set ado_express as working directory:
        "cd ado_express"
5. Start app:
        "python main.py"

## VS Code Development Container
    If you wish to run this app without any installations, you can do so by running your local development environment inside a container. 
    
    Steps:
    1. In the root directory press F1
    2. Search for "Dev Containers: Rebuild and Reopen in Container" and press enter

    **Make sure the environment variables & deployment plan is set before running the development container.