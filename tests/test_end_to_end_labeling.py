# tests/test_end_to_end_labeling.py
import os
import re
import time

import yaml
import pytest
from playwright.sync_api import Page, expect

# ======================
# 配置
# ======================
BASE_URL = "http://127.0.0.1:8000"
EMAIL = "1034477689@qq.com"
PASSWORD = "258258Www"


# ======================
# 工具函数（不是 fixture！）
# ======================
def load_test_cases():
    """从 YAML 文件加载测试用例"""
    test_dir = os.path.dirname(__file__)
    data_file = os.path.join(test_dir, "test_data", "labeling_cases.yaml")
    with open(data_file, encoding="utf-8") as f:
        cases = yaml.safe_load(f)
    # 注入完整图片路径
    data_dir = os.path.join(test_dir, "data")
    for case in cases:
        case["image_path"] = os.path.join(data_dir, case["image"])
        assert os.path.exists(case["image_path"]), f"图片不存在: {case['image_path']}"
    return cases


# ======================
# Fixtures
# ======================
@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


# ======================
# 测试用例（参数化）
# ======================
@pytest.mark.parametrize(
    "case",
    load_test_cases(),
    ids=lambda c: c["task_name"]  # 用任务名作为用例 ID
)
def test_create_task_and_label_image(page: Page, case, base_url):
    task_name = case["task_name"]
    image_path = case["image_path"]
    points = case["points"]

    # === 1. 登录 ===
    page.goto(f"{base_url}/login")
    page.get_by_placeholder("Email邮箱地址").fill(EMAIL)
    page.get_by_placeholder("密码").fill(PASSWORD)
    page.get_by_role("button", name=re.compile(r"登\s*录")).click()
    expect(page.get_by_role("button", name="新建任务")).to_be_visible(timeout=10000)

    # === 2. 创建任务 ===
    page.get_by_role("button", name="新建任务").click()

    try:
        page.get_by_placeholder("请输入50字以内的任务名称").fill(task_name)
    except:
        page.locator("input").first.fill(task_name)

    try:
        page.get_by_label("数据类型").click()
    except:
        page.locator("div").filter(has_text="* 数据类型 :").locator(
            "xpath=..//input | ..//div[contains(@class, 'ant-select')]"
        ).first.click()

    page.get_by_text("图片").click()
    page.get_by_role("button", name="下一步").click()

    # === 3. 上传图片 ===
    page.get_by_role("button", name="file Choose File 上传文件").get_by_role("button").set_input_files(image_path)
    # 等待文件名出现在页面上（假设 LabelU 会显示文件名）
    filename = os.path.basename(image_path)
    time.sleep(1)
    # page.wait_for_selector(f"{filename}", timeout=20)
    page.get_by_role("button", name="下一步").click()
    # === 4. 设置标注类型 ===
    page.locator('//*[@id="rc_select_2"]').click()
    page.get_by_text("标点").click()
    page.get_by_role("button", name=re.compile(r"保\s*存")).click()

    # === 5. 开始标注 ===
    page.wait_for_selector("button:has-text('开始标注')", timeout=15000)
    page.get_by_role("button", name="开始标注").click()

    canvas = page.locator("canvas").first
    expect(canvas).to_be_visible(timeout=10000)
    for x, y in points:
        canvas.click(position={"x": x, "y": y})

    page.get_by_role("button", name=re.compile(r"完\s*成")).click()
    page.get_by_role("button", name="返回样本列表").click()

    # === 6. 验证标注状态 ===
    expect(page.get_by_text("已标注")).to_be_visible(timeout=10000)

    print(f"✅ 测试通过: {task_name}")