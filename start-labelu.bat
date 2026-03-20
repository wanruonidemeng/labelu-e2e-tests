@echo off
REM
cd /d  C:\Users\zpl\PycharmProjects\PycharmProjects\yann
call conda activate labelu
labelu --port 8000 > nul 2>&1 &
timeout /t 15 /nobreak >nul
echo LabelU started on port 8000