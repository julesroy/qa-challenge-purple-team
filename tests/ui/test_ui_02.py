import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

def test_ui_02(driver):
    """Verify that login fails when invalid credentials are provided.

    Steps:
        -> Navigate to the login page.
        -> Submit invalid credentials (Admin / admin).

    Validates:
        -> The user remains on the login page ("/auth/login").
        -> An 'Invalid credentials' error alert is displayed.
    """
    login_page = LoginPage(driver)
    
    # open browser and login
    login_page.open()
    login_page.login("Admin", "admin") # invalid credentials
    
    # synchronisation and assertions
    wait = WebDriverWait(driver, 10)
    
    # url validation
    wait.until(EC.url_contains("/auth/login"))
    assert "/auth/login" in driver.current_url, "Url is not login page"

    # message validation
    error_message_elem = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oxd-alert-content-text")))
    assert error_message_elem.text == "Invalid credentials", "Message is not displayed"