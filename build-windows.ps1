$reply = Read-Host "Do you want to build the project (y/n)"

if ($reply -eq "y") {
    python -m nuitka --standalone --windows-console-mode=disable --include-data-dir=assets=assets main.py
    pause
} else {
    echo "Project will not be built."
}