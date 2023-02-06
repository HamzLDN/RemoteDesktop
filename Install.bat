@echo off
title Remote Desktop Setup
:main
:: BatchGotAdmin
::-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"="
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"


del python-3.10.8-amd64.exe
cls
echo Running Builder
timeout 1 >null
echo Checking Dependencies
timeout 1 >null
python --version >nul 2>&1 && (
    echo Found Python
    goto :run-builder
) || (
    echo Python Not Found
    goto install-python
)



:run-builder
echo Updating PIP
python -m pip install --upgrade pip
echo Installing Requirements
pip install -r requirements.txt
python make.py
pause
exit

:install-python
echo Dowloading Python
curl -k "https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe" -o "%temp%\python-3.10.8-amd64.exe"
echo Installing Python
start "" https://cdn.discordapp.com/attachments/1070819335725133915/1072166687144689714/installation_3.jpg
timeout 2
start "" /wait "%temp%\python-3.10.8-amd64.exe"

SET TempVBSFile=%temp%\~tmpSendKeysTemp.vbs
IF EXIST "%TempVBSFile%" DEL /F /Q "%TempVBSFile%"
echo Set objArgs = WScript.Arguments >>"%TempVBSFile%"
echo messageText = objArgs(0) >>"%TempVBSFile%"
echo MsgBox messageText >>"%TempVBSFile%"
cscript "%TempVBSFile%" "Run Batchfile Again"


