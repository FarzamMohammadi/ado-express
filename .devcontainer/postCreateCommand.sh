python --version
pip3 install --upgrade pip
pip3 install --user -r /workspaces/ado-express/requirements.txt
if [ -f files/logs/deployment.log ]; then 
    cat files/logs/deployment.log >> files/logs/deployment-stale.log
fi
echo > files/logs/deployment.log
tail -f files/logs/deployment.log & python ado_express/main.py