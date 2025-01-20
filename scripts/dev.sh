#!/bin/bash

run_planeframe() {
    rsync -qauz .. planeframe:/home/jeffery/planeframe/ --exclude dev.sh --exclude promote.sh --exclude .git --exclude venv --exclude __pycache__
    echo " / ⬆️"
    ssh -o ControlMaster=auto -o ControlPath=/tmp/ssh-%r@%h:%p -o ControlPersist=1h planeframe "cd /home/jeffery/planeframe && source venv/bin/activate && python3 flight_tracker.py"
}

run_planeframe

fswatch -o ../*.py | while read f; do
    echo -n "🔄"
    run_planeframe
done
