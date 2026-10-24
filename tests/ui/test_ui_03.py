import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.pim_page import PimPage

def test_ui_03(driver):
    """Verify employee creation with an uploaded profile picture.

    Steps:
        -> Log in as Admin and navigate to the PIM Add Employee page.
        -> Fill in first and last names, and upload an avatar image.
        -> Save the new employee record.

    Validates:
        -> A 'Successfully Saved' toast notification appears.
        -> The browser redirects to the personal details profile page ("/pim/viewPersonalDetails").
        -> The uploaded avatar is visible on the profile page.
    """
    login_page = LoginPage(driver)
    pim_page = PimPage(driver)
    wait = WebDriverWait(driver, 10)

    # 1. Login as Admin
    login_page.open()
    login_page.login("Admin", "admin123")

    wait.until(EC.url_contains("/dashboard/index"))
    pim_page.navigate_to_add_employee()

    # enter details and upload avatar
    avatar_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "avatar.jpg")
    pim_page.add_employee("John", "Doe", avatar_path=avatar_path)

    # validations
    # validate success toast message
    toast_text = pim_page.get_toast_message()
    assert "Successfully Saved" in toast_text, f"Expected success message but got: {toast_text}"

    # validate redirection to personal details profile page
    wait.until(EC.url_contains("/pim/viewPersonalDetails"))
    assert "/pim/viewPersonalDetails" in driver.current_url, "URL does not contain personal details path"

    # validate avatar is displayed
    assert pim_page.is_avatar_displayed(), "Employee avatar is not displayed on profile page"
