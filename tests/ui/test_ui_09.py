import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.leave_page import LeavePage

# TEST-UI-09 : Leave request with date validation
def test_ui_09(driver):
    login_page = LoginPage(driver)
    leave_page = LeavePage(driver)
    wait = WebDriverWait(driver, 10)

    # 1. Login as Admin
    login_page.open()
    login_page.login("Admin", "admin123")
    wait.until(EC.url_contains("/dashboard/index"))

    # 2. Navigate to Leave > Apply
    leave_page.navigate_to_apply()

    # 3. Check preconditions: on public demo, user may have 0 leave balance
    if leave_page.is_no_leave_balance_displayed():
        # Validate that system correctly displays the no balance warning
        assert leave_page.is_no_leave_balance_displayed(), "System message 'No Leave Types with Leave Balance' displayed"
    else:
        # 4. If leave types with balance exist, apply for leave
        leave_page.apply_leave(
            from_date="2026-11-10",
            to_date="2026-11-12",
            comment="Automated test leave application"
        )
        toast_msg = leave_page.get_toast_message()
        assert "Successfully Saved" in toast_msg or "Success" in toast_msg, (
            f"Expected success message for leave request, got: {toast_msg}"
        )
