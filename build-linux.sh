#!/bin/bash

echo "This script is not supported anymore, and does not have the same features as the windows script"
read -r -p "Do you want to build the project: (y/n)"

if  [ $INPUT = "y" ]; then
    read -r -p "Do you want to get the python dependancies? (y/n)"
    if  [ $INPUT = "y" ]; then
        pip -install -r requirements-build.txt
    fi
    python -m nuitka --standalone --include-data-dir=assets=assets --deployment --python-flag=no_site,no_asserts,no_docstrings,no_warnings --main=main.py
    read -n 1 -s -r -p "Press any key to continue"
else
    echo "Project will not be built."
fi
