@echo off
REM 
cd /d %~dp0

REM 直接使用 Python 安装的 labelu（假设已通过 pip 安装）
labelu.exe --port 8000 > nul 2>&1

REM 等待服务启动
timeout /t 15 /nobreak >nul

echo LabelU started on http://localhost:8000
