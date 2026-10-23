import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pytest_html import extras

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # options.add_argument("--headless=new") # uncomment if we want to run in background (no window)
    
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras_list = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        # Capture screenshot if driver fixture is present
        driver = item.funcargs.get("driver", None)
        if driver:
            try:
                screenshot_b64 = driver.get_screenshot_as_base64()
                extras_list.append(extras.image(screenshot_b64, name="Screenshot on Failure"))
                html_preview = f'<div><p><strong>Screenshot on Failure:</strong></p><img src="data:image/png;base64,{screenshot_b64}" alt="Failure Screenshot" style="max-width:600px; border:1px solid #ccc; border-radius:4px; margin-top:5px;" /></div>'
                extras_list.append(extras.html(html_preview))
            except Exception as e:
                print(f"[conftest] Impossible de capturer le screenshot : {e}")

    report.extras = extras_list

def pytest_html_report_title(report):
    report.title = "QA Challenge - Test Execution Report"
