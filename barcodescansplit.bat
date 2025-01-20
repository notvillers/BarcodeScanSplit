@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Initialize variables
set "SOURCE="
set "DESTINATION="
set "BACKUP="
set "LOG="
set "TEMP="
set "IMAGE="
set "MODE="
set "PROCESSES=%NUMBER_OF_PROCESSORS%"

REM Function to display usage
:display_usage
    echo Usage: %~n0 [OPTIONS]
    echo.
    echo Options:
    echo   -s, --source       Directory containing PDF files.
    echo   -d, --destination  Directory to store output files.
    echo   -b, --backup       Directory to store backup files.
    echo   -l, --log          Directory to store log files.
    echo   -t, --temp         Temporary directory to store split files.
    echo   -i, --image        Temporary directory to store images.
    echo   -m, --mode         Processing mode (single or multi).
    echo   -p, --processes    Maximum number of processes to run (default: number of CPU threads).
    echo   -h, --help         Display this help message and exit.
    echo.
    echo Example: %~n0 -s "C:\Source" -d "C:\Dest" -m single
    exit /b 1

REM Parse arguments
:parse_args
if "%~1"=="" goto end_args

if "%~1"=="--source" (set "SOURCE=%~2" & shift & shift & goto parse_args)
if "%~1"=="-s" (set "SOURCE=%~2" & shift & shift & goto parse_args)
if "%~1"=="--destination" (set "DESTINATION=%~2" & shift & shift & goto parse_args)
if "%~1"=="-d" (set "DESTINATION=%~2" & shift & shift & goto parse_args)
if "%~1"=="--backup" (set "BACKUP=%~2" & shift & shift & goto parse_args)
if "%~1"=="-b" (set "BACKUP=%~2" & shift & shift & goto parse_args)
if "%~1"=="--log" (set "LOG=%~2" & shift & shift & goto parse_args)
if "%~1"=="-l" (set "LOG=%~2" & shift & shift & goto parse_args)
if "%~1"=="--temp" (set "TEMP=%~2" & shift & shift & goto parse_args)
if "%~1"=="-t" (set "TEMP=%~2" & shift & shift & goto parse_args)
if "%~1"=="--image" (set "IMAGE=%~2" & shift & shift & goto parse_args)
if "%~1"=="-i" (set "IMAGE=%~2" & shift & shift & goto parse_args)
if "%~1"=="--mode" (set "MODE=%~2" & shift & shift & goto parse_args)
if "%~1"=="-m" (set "MODE=%~2" & shift & shift & goto parse_args)
if "%~1"=="--processes" (set "PROCESSES=%~2" & shift & shift & goto parse_args)
if "%~1"=="-p" (set "PROCESSES=%~2" & shift & shift & goto parse_args)
if "%~1"=="--help" (goto display_usage)
if "%~1"=="-h" (goto display_usage)

echo Unknown option: %~1
exit /b 1

:end_args

REM Validate required arguments
if "%SOURCE%"=="" (
    echo Error: -s/--source is required.
    goto display_usage
)
if "%DESTINATION%"=="" (
    echo Error: -d/--destination is required.
    goto display_usage
)
if "%MODE%"=="" (
    echo Error: -m/--mode is required.
    goto display_usage
)

REM Print parsed arguments
echo Source directory: %SOURCE%
echo Destination directory: %DESTINATION%
echo Backup directory: %BACKUP%
echo Log directory: %LOG%
echo Temporary directory for splits: %TEMP%
echo Temporary directory for images: %IMAGE%
echo Processing mode: %MODE%
echo Maximum processes: %PROCESSES%

REM Add your processing logic below this line
REM ...