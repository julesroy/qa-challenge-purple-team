import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # URLs
        self.users_url = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers"
        self.add_user_url = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser"
        self.pay_grades_url = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewPayGrades"

        # Sidebar & Top nav
        self._admin_menu = (By.XPATH, "//span[text()='Admin']")

        # User management selectors
        self._search_username_input = (By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input")
        self._search_submit_btn = (By.CSS_SELECTOR, "button[type='submit']")
        self._table_body = (By.CSS_SELECTOR, ".oxd-table-body")
        self._delete_icon_btn = (By.CSS_SELECTOR, "button .bi-trash")
        self._confirm_delete_btn = (By.XPATH, "//button[contains(., 'Yes, Delete')] | //button[contains(@class, 'oxd-button--label-danger')]")

        # Add user form selectors
        self._role_select = (By.XPATH, "//label[text()='User Role']/parent::div/following-sibling::div//div[contains(@class, 'oxd-select-text')]")
        self._status_select = (By.XPATH, "//label[text()='Status']/parent::div/following-sibling::div//div[contains(@class, 'oxd-select-text')]")
        self._employee_name_input = (By.XPATH, "//label[text()='Employee Name']/parent::div/following-sibling::div//input")
        self._autocomplete_option = (By.CSS_SELECTOR, ".oxd-autocomplete-dropdown div[role='option'] span")
        self._username_field = (By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input")
        self._password_field = (By.XPATH, "//label[text()='Password']/parent::div/following-sibling::div//input")
        self._confirm_password_field = (By.XPATH, "//label[text()='Confirm Password']/parent::div/following-sibling::div//input")
        self._save_user_btn = (By.CSS_SELECTOR, "button[type='submit']")

        # Pay Grades selectors
        self._edit_pay_grade_icon = (By.CSS_SELECTOR, ".bi-pencil-fill")
        self._add_currency_btn = (By.XPATH, "//h6[text()='Currencies']/following::button[contains(., 'Add')][1]")
        self._min_salary_input = (By.XPATH, "//label[text()='Minimum Salary']/parent::div/following-sibling::div//input")
        self._max_salary_input = (By.XPATH, "//label[text()='Maximum Salary']/parent::div/following-sibling::div//input")
        self._inline_error_msg = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

        # Toast
        self._toast_message = (By.CSS_SELECTOR, ".oxd-text--toast-message, .oxd-toast-content, .oxd-toast")

    def navigate_to_users(self):
        """Navigate to Admin > User Management > Users."""
        self.driver.get(self.users_url)
        self.wait.until(EC.visibility_of_element_located(self._search_username_input))

    def navigate_to_add_user(self):
        """Navigate directly to the Add User page."""
        self.driver.get(self.add_user_url)
        self.wait.until(EC.visibility_of_element_located(self._role_select))

    def navigate_to_pay_grades(self):
        """Navigate to Admin > Job > Pay Grades."""
        self.driver.get(self.pay_grades_url)
        self.wait.until(EC.visibility_of_element_located(self._edit_pay_grade_icon))

    def open_first_pay_grade_edit(self):
        """Click on the edit icon of the first pay grade in the table."""
        edit_icon = self.wait.until(EC.element_to_be_clickable(self._edit_pay_grade_icon))
        edit_icon.click()
        self.wait.until(EC.url_contains("/payGrade/"))

    def open_add_currency(self):
        """Click the Add button in the Currencies section."""
        btn = self.wait.until(EC.element_to_be_clickable(self._add_currency_btn))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()
        self.wait.until(EC.visibility_of_element_located(self._min_salary_input))

    def _select_dropdown(self, locator, option_text):
        dropdown = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
        dropdown.click()
        time.sleep(0.5)
        option_xpath = f"//div[@role='option']//span[text()='{option_text}']"
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()

    def search_user(self, username: str):
        """Search for a user in the user management table."""
        input_elem = self.wait.until(EC.element_to_be_clickable(self._search_username_input))
        input_elem.clear()
        input_elem.send_keys(username)
        self.driver.find_element(*self._search_submit_btn).click()
        time.sleep(1.5)

    def delete_first_user_in_table(self):
        """Click delete on the first user in search results and confirm on modal."""
        delete_btn = self.wait.until(EC.element_to_be_clickable(self._delete_icon_btn))
        delete_btn.click()
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self._confirm_delete_btn))
        confirm_btn.click()

    def create_user(self, role: str, status: str, username: str, password: str, employee_hint: str = "a"):
        """Fill in and submit the Add User form."""
        self._select_dropdown(self._role_select, role)
        self._select_dropdown(self._status_select, status)

        # Autocomplete employee name
        emp_input = self.wait.until(EC.element_to_be_clickable(self._employee_name_input))
        emp_input.clear()
        emp_input.send_keys(employee_hint)
        # Wait for real autocomplete suggestions (span inside option)
        first_option = self.wait.until(EC.element_to_be_clickable(self._autocomplete_option))
        first_option.click()

        # Username
        user_input = self.wait.until(EC.element_to_be_clickable(self._username_field))
        user_input.send_keys(username)

        # Passwords
        pwd_input = self.wait.until(EC.element_to_be_clickable(self._password_field))
        pwd_input.send_keys(password)
        confirm_pwd = self.wait.until(EC.element_to_be_clickable(self._confirm_password_field))
        confirm_pwd.send_keys(password)

        # Submit
        save_btn = self.wait.until(EC.element_to_be_clickable(self._save_user_btn))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        save_btn.click()

    def test_pay_grade_salary_validation(self, min_salary: str, max_salary: str):
        """Fill salary boundary values and return inline error message."""
        min_input = self.wait.until(EC.element_to_be_clickable(self._min_salary_input))
        min_input.clear()
        min_input.send_keys(str(min_salary))

        max_input = self.wait.until(EC.element_to_be_clickable(self._max_salary_input))
        max_input.clear()
        max_input.send_keys(str(max_salary))
        # Trigger validation via tab or submit click
        max_input.send_keys(Keys.TAB)
        try:
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        except Exception:
            pass

    def get_inline_error_message(self):
        """Retrieve the inline validation error text."""
        error = self.wait.until(EC.visibility_of_element_located(self._inline_error_msg))
        return error.text

    def get_toast_message(self):
        """Retrieve toast notification text."""
        toast = self.wait.until(EC.visibility_of_element_located(self._toast_message))
        return toast.text
