import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.my_info_page import MyInfoPage

# TEST-UI-05 : Reject unauthorized file upload
def test_ui_05(driver):
    login_page = LoginPage(driver)
    my_info_page = MyInfoPage(driver)
    wait = WebDriverWait(driver, 10)

    # 1. Login as Admin
    login_page.open()
    login_page.login("Admin", "admin123")
    wait.until(EC.url_contains("/dashboard/index"))

    # 2. Navigate to My Info (Personal Details)
    my_info_page.navigate()

    # 3. Open attachment section and attempt upload of unauthorized executable
    payload_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "script_payload.exe")
    my_info_page.open_add_attachment()
    my_info_page.upload_attachment(file_path=payload_path, comment="Unauthorized payload test")

    # 4. Validations
    # Check that either an error message is visible or the file is not present in attachments table
    error_displayed = False
    try:
        error_msg = my_info_page.get_inline_error_message()
        if error_msg:
            error_displayed = True
    except Exception:
        pass

    assert error_displayed or not my_info_page.has_attachment("script_payload.exe"), (
        "Unauthorized file script_payload.exe was unexpectedly accepted or saved without error"
    )
