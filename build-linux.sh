#!/bin/bash

read ans -r -p "Do you want to build the project (y/n)"

if  [$ans = "y"]; then
    #python -m nuitka --standalone --windows-console-mode=disable --include-data-dir=assets=assets main.py
    read -n 1 -s -r -p "Press any key to continue"
else
    echo "Project will not be built."
fi
