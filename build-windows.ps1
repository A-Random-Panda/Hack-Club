$reply = Read-Host "Do you want to build the project (y/n)"

if ($reply -eq "y") {
    $reply = Read-Host "Do you want to get the python dependancies? (y/n)"
    if ($reply -eq "y") {
        pip -install -r requirements-build.txt
    }
    $reply = Read-Host "Deployment build (y/n)"
    if ($reply -eq "n") {
        python -m nuitka --standalone --include-data-dir=assets=assets --main=main.py
        pause
    }
    if ($reply -eq "y") {
        python -m nuitka --standalone --windows-console-mode=disable --deployment --include-data-dir=assets=assets --python-flag=isolated,no_asserts,no_docstrings,no_warnings --main=main.py
        pause
    }
} else {
    echo "Project will not be built."
}