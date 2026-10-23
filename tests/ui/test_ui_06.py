import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.my_info_page import MyInfoPage

# TEST-UI-06 : Personal details update
def test_ui_06(driver):
    login_page = LoginPage(driver)
    my_info_page = MyInfoPage(driver)
    wait = WebDriverWait(driver, 10)

    # 1. Login as Admin
    login_page.open()
    login_page.login("Admin", "admin123")
    wait.until(EC.url_contains("/dashboard/index"))

    # 2. Navigate to My Info
    my_info_page.navigate()

    # 3. Update personal details (format yyyy-dd-mm)
    my_info_page.update_personal_details(
        nationality="French",
        marital_status="Single",
        dob="1995-12-05"
    )

    # 4. Validations
    toast_text = my_info_page.get_toast_message()
    assert "Successfully Updated" in toast_text, f"Expected 'Successfully Updated' toast, got: {toast_text}"
