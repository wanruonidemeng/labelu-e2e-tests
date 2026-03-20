# tests/conftest.py
import subprocess
import time
import atexit
import requests
import sys
import os

# 将当前项目目录加入 Python 路径（如果需要）
sys.path.insert(0, os.path.dirname(__file__))

_labelu_process = None

def start_labelu():
    global _labelu_process
    if _labelu_process is None:
        print("Starting LabelU service...")
        # 启动 labelu（不重定向，由 pytest 管理生命周期）
        _labelu_process = subprocess.Popen(
            [sys.executable, "-m", "labelu.cmd.server", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        # 等待服务就绪（最多30秒）
        for i in range(30):
            try:
                resp = requests.get("http://localhost:8000/docs", timeout=1)
                if resp.status_code == 200:
                    print("LabelU is ready!")
                    return
            except:
                time.sleep(1)
        raise RuntimeError("LabelU failed to start after 30 seconds")

def stop_labelu():
    global _labelu_process
    if _labelu_process:
        print("Stopping LabelU...")
        _labelu_process.terminate()
        try:
            _labelu_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _labelu_process.kill()
        _labelu_process = None

# 自动启停
start_labelu()
atexit.register(stop_labelu)
