import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.admin_page import AdminPage

# TEST-UI-07 : Pay grade boundary validation
def test_ui_07(driver):
    login_page = LoginPage(driver)
    admin_page = AdminPage(driver)
    wait = WebDriverWait(driver, 10)

    # 1. Login as Admin
    login_page.open()
    login_page.login("Admin", "admin123")
    wait.until(EC.url_contains("/dashboard/index"))

    # 2. Navigate to Admin > Job > Pay Grades
    admin_page.navigate_to_pay_grades()

    # 3. Open existing pay grade to edit
    admin_page.open_first_pay_grade_edit()

    # 4. Open Add Currency section
    admin_page.open_add_currency()

    # 5. Input boundary salary values: minSalary (50000) > maxSalary (30000)
    admin_page.test_pay_grade_salary_validation(min_salary="50000", max_salary="30000")

    # 6. Validations
    error_msg = admin_page.get_inline_error_message()
    assert "Should be higher than Minimum Salary" in error_msg, (
        f"Expected 'Should be higher than Minimum Salary' validation message, got: {error_msg}"
    )
