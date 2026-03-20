@echo off
REM
cd /d %~dp0
call conda activate labelu
labelu --port 8000 > nul 2>&1 &
timeout /t 15 /nobreak >nul
echo LabelU started on port 8000
