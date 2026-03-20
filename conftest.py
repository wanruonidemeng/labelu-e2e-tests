# conftest.py
import pytest
from playwright.sync_api import Browser, BrowserContext, Page


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    # 只设置 headless=False（调试时），其他交给 pytest-playwright
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        # 如果你想始终显示浏览器（开发时）：
        # headless=False
    )
    yield context
    context.close()
# 在 conftest.py 中添加
@pytest.fixture(autouse=True)
def auto_screenshot_on_failure(page: Page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"test-results/{request.node.name}.png")
        page.context.tracing.stop(path=f"test-results/{request.node.name}.zip")