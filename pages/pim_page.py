import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PimPage:
    """Page object for the PIM section of the website."""
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.add_employee_url = "https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee"

        # navigation selectors
        self._pim_menu_link = (By.XPATH, "//span[text()='PIM']")
        self._add_employee_tab = (By.XPATH, "//a[text()='Add Employee']")

        # form selectors
        self._first_name_input = (By.NAME, "firstName")
        self._last_name_input = (By.NAME, "lastName")
        self._file_input = (By.CSS_SELECTOR, "input[type='file']")
        self._save_button = (By.CSS_SELECTOR, "button[type='submit']")

        # confirmation / assertions selectors
        self._toast_message = (By.CSS_SELECTOR, ".oxd-text--toast-message, .oxd-toast-content")
        self._employee_image = (By.CSS_SELECTOR, ".orangehrm-edit-employee-image img, img.employee-image")

    def navigate_to_add_employee(self):
        """Navigate to Add Employee either via top navigation or directly via URL."""
        try:
            pim_link = self.wait.until(EC.element_to_be_clickable(self._pim_menu_link))
            pim_link.click()
            add_tab = self.wait.until(EC.element_to_be_clickable(self._add_employee_tab))
            add_tab.click()
        except Exception:
            # we fallback to direct navigation if menu is slow
            self.driver.get(self.add_employee_url)

        self.wait.until(EC.visibility_of_element_located(self._first_name_input))

    def add_employee(self, first_name: str, last_name: str, avatar_path: str = None):
        """Fill in employee details, optionally attach avatar, and submit."""
        first_name_elem = self.wait.until(EC.element_to_be_clickable(self._first_name_input))
        first_name_elem.clear()
        first_name_elem.send_keys(first_name)

        last_name_elem = self.wait.until(EC.element_to_be_clickable(self._last_name_input))
        last_name_elem.clear()
        last_name_elem.send_keys(last_name)

        if avatar_path:
            abs_path = os.path.abspath(avatar_path)
            file_elem = self.wait.until(EC.presence_of_element_located(self._file_input))
            file_elem.send_keys(abs_path)

        save_btn = self.wait.until(EC.element_to_be_clickable(self._save_button))
        save_btn.click()

    def get_toast_message(self):
        """Retrieve text from the success notification toast."""
        toast = self.wait.until(EC.visibility_of_element_located(self._toast_message))
        return toast.text

    def is_avatar_displayed(self):
        """Check if profile avatar image is displayed on the profile page."""
        image = self.wait.until(EC.visibility_of_element_located(self._employee_image))
        return image.is_displayed()
