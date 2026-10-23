import os
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.my_info_page import MyInfoPage

# TEST-UI-04 : Add attachment to employee profile
def test_ui_04(driver):
    login_page = LoginPage(driver)
    my_info_page = MyInfoPage(driver)
    wait = WebDriverWait(driver, 10)

    # 1. Login as Admin
    login_page.open()
    login_page.login("Admin", "admin123")
    wait.until(EC.url_contains("/dashboard/index"))

    # 2. Navigate to My Info (Personal Details)
    my_info_page.navigate()

    # 3. Open attachment section and upload contract.pdf
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "contract.pdf")
    my_info_page.open_add_attachment()
    my_info_page.upload_attachment(file_path=pdf_path, comment="Employment contract")

    # 4. Validations
    # Verify that the document appears in the attachments table or success toast is triggered
    assert my_info_page.has_attachment("contract.pdf"), "Attachment contract.pdf is not listed in table"
