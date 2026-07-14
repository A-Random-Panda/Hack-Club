#!/bin/bash

read -r -p "Do you want to build the project: (y/n)"

if  [ $INPUT = "y" ]; then
    python -m nuitka --standalone --include-data-dir=assets=assets main.py
    read -n 1 -s -r -p "Press any key to continue"
else
    echo "Project will not be built."
fi
