import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

def test_ui_01(driver):
    """Verify that a user can successfully log in with valid credentials.

    Steps:
        -> Navigate to the login page.
        -> Submit valid credentials (Admin / admin123).

    Validates:
        -> The user is redirected to the dashboard page ("/dashboard/index").
    """
    login_page = LoginPage(driver)
    
    # open browser and login
    login_page.open()
    login_page.login("Admin", "admin123") # valid credentials
    
    # synchronisation and assertions
    wait = WebDriverWait(driver, 10)
    
    # url validation
    wait.until(EC.url_contains("/dashboard/index"))
    assert "/dashboard/index" in driver.current_url, "Url is not dashboard"