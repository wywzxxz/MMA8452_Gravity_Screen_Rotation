@echo off
cd /d "%~dp0"
start /B pythonw server.py > NUL 2>&1
exit