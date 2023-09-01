@echo off
setlocal enabledelayedexpansion

rem Set the path to your Python executable
set "python_executable=python3"

rem Set the path to your requirements.txt file (assuming it's in the same folder as the script)
set "script_directory=%~dp0"
set "requirements_file=%script_directory%requirements.txt"

rem Initialize the error flag
set "error_flag=0"

rem Install Python packages from requirements.txt
@REM %python_executable% -m pip install -r %requirements_file%
python -m pip install -r requirements.txt || (
    echo [ERROR] Package installation failed.
    set "error_flag=1"
)


rem Set the folder path containing the Python files
set "folder_path=%script_directory%/../"

rem Read the list of Python files from custom_requirements.txt
set "file_list=custom_requirements.txt"

rem Loop through the list of Python files and check if each file exists
for /f %%f in (%file_list%) do (
    if not exist "%folder_path%\%%f" (
        echo [ERROR] File missing: %%f does not exist in the folder.
        set "error_flag=1"
    )
)

if %error_flag% equ 1 (
    echo Installation failed.
) else (
    echo Installation successful.
)

rem Prompt user to press Enter to close the terminal
pause

endlocal
