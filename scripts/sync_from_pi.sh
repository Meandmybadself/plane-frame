#!/bin/bash

rsync -av planeframe:/home/jeffery/planeframe/ $HOME/Sites/planeframe/ --exclude .git --exclude venv --exclude __pycache__