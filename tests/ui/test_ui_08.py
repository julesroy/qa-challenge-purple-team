import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.admin_page import AdminPage

def test_ui_08(driver):
    """Verify user deletion through confirmation modal dialog.

    Steps:
        -> Log in as Admin and navigate to Admin > User Management.
        -> Trigger the delete action on a user row and confirm the deletion modal dialog.

    Validates:
        -> A success toast notification ('Successfully Deleted' / 'Success') is displayed.
    """
    login_page = LoginPage(driver)
    admin_page = AdminPage(driver)
    wait = WebDriverWait(driver, 10)

    # 1. Login as Admin
    login_page.open()
    login_page.login("Admin", "admin123")
    wait.until(EC.url_contains("/dashboard/index"))

    # 2. Navigate to Admin > User Management
    admin_page.navigate_to_users()

    # 3. Search for test user or ensure table is populated
    table_elem = wait.until(EC.visibility_of_element_located(admin_page._table_body))
    assert table_elem.is_displayed(), "User table is not displayed"

    # 4. Trigger deletion on target row and confirm modal dialog
    admin_page.delete_first_user_in_table()

    # 5. Validations
    toast_msg = admin_page.get_toast_message()
    assert "Successfully Deleted" in toast_msg or "Success" in toast_msg, (
        f"Expected deletion confirmation toast, got: {toast_msg}"
    )
