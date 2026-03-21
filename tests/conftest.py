import pytest
import requests
import time

@pytest.fixture(scope="session", autouse=True)
def ensure_labelu_is_ready():
    """假设 LabelU 已由 CI 启动，只需等待就绪"""
    for i in range(60):
        try:
            resp = requests.get("http://localhost:8000/docs", timeout=1)
            if resp.status_code == 200:
                return
        except:
            pass
        time.sleep(1)
    pytest.fail("LabelU service not ready after 60 seconds")
