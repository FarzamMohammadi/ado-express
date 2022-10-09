pip3 install --user -r requirements.txt
if [ -f deployment.log ]; then 
    cat deployment.log >> deployment_stale.log 
fi
echo > deployment.log
tail -f deployment.log & python update_releases.py