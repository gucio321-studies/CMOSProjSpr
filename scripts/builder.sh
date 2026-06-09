#!/bin/bash
# For use with JetBrains IDE (or anything else)
# run this from root of sphinx project and it should build and run it with okular pdf veiwer.
PWD=$PWD
echo $PWD

if [ ! -d $PWD/venv ]; then
    python3 -m virtualenv $PWD/venv
    source $PWD/venv/bin/activate
    python3 -m pip install -r requirements.txt
    python3 -m pip install setuptools
fi

source $PWD/venv/bin/activate
# extract file name from conf.py
# file name is of form lowercased value of "project" variable
# and .pdf extension
# e.g. project = 'MyProject' -> myproject.pdf
filename=$(grep project $PWD/conf.py | sed -e "s/.*'\(.*\)'.*/\L\1.pdf/")
echo $filename
filepath=$PWD/_build/latex/$filename
make latexpdf
okular $filepath
