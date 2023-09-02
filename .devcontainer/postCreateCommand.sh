#!/usr/bin/env bash

python --version
pip3 install --upgrade pip
pip3 install --user -r /workspaces/ado-express/requirements.txt

if [ -f ado_express/files/logs/deployment.log ]; then 
    cat ado_express/files/logs/deployment.log >> ado_express/files/logs/deployment-stale.log
fi

echo > ado_express/files/logs/deployment.log
python ado_express/main.py