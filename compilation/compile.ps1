# # PWD should be the same directory is this file resides

$ScriptPath = split-path -parent $MyInvocation.MyCommand.Definition

$VENV_PATH= (Join-Path (Split-Path -Parent $ScriptPath) -ChildPath "venv")

#!/bin/bash
$ModuleName = "punctual"
$EXE_NAME="punc"
$INCLUDE_PATHS="../"
$SCRIPT_FILE="../cli.py"

$ArgList = @(
    "-y", "--clean", "--console", "--onefile",
    "--name=$EXE_NAME", "--paths=$INCLUDE_PATHS",
    "--collect-submodules=$ModuleName", $SCRIPT_FILE
)

Start-Process -FilePath "$VENV_PATH\Scripts\pyinstaller.exe" -ArgumentList $ArgList -Wait -NoNewWindow

.\dist\punc.exe

