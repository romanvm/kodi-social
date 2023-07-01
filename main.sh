#!/bin/bash

set -e

PROJECT_PATH=/home/roman/kodi-social

cd $PROJECT_PATH
source .venv/bin/activate

python main.py -u
