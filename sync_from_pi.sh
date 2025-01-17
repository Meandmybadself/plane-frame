#!/bin/bash

rsync -av planeframe:/home/jeffery/planeframe/ . --exclude .git --exclude venv --exclude __pycache__
