import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LeavePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.apply_leave_url = "https://opensource-demo.orangehrmlive.com/web/index.php/leave/applyLeave"
        self.my_leave_url = "https://opensource-demo.orangehrmlive.com/web/index.php/leave/viewMyLeaveList"

        # Card header
        self._card_header = (By.XPATH, "//h6[contains(., 'Apply Leave')]")

        # Form selectors
        self._leave_type_select = (By.XPATH, "//label[text()='Leave Type']/parent::div/following-sibling::div//div[contains(@class, 'oxd-select-text')]")
        self._from_date_input = (By.XPATH, "//label[text()='From Date']/parent::div/following-sibling::div//input")
        self._to_date_input = (By.XPATH, "//label[text()='To Date']/parent::div/following-sibling::div//input")
        self._comments_textarea = (By.XPATH, "//label[text()='Comments']/parent::div/following-sibling::div//textarea")
        self._submit_btn = (By.CSS_SELECTOR, "button[type='submit']")

        # Toast
        self._toast_message = (By.CSS_SELECTOR, ".oxd-text--toast-message, .oxd-toast-content, .oxd-toast")

    def navigate_to_apply(self):
        """Navigate to Leave > Apply and wait for the card to render."""
        self.driver.get(self.apply_leave_url)
        self.wait.until(EC.visibility_of_element_located(self._card_header))

    def is_no_leave_balance_displayed(self):
        """Check if 'No Leave Types with Leave Balance' notice is shown."""
        card = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-card-container")
        return "No Leave Types with Leave Balance" in card.text

    def _select_first_leave_type(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self._leave_type_select))
        dropdown.click()
        time.sleep(0.5)
        first_option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-select-dropdown div[role='option']:not(:first-child)")))
        first_option.click()

    def apply_leave(self, from_date: str, to_date: str, comment: str = None):
        """Fill and submit leave request."""
        self._select_first_leave_type()

        from_elem = self.wait.until(EC.element_to_be_clickable(self._from_date_input))
        from_elem.send_keys(Keys.COMMAND if "darwin" in os.sys.platform else Keys.CONTROL, "a")
        from_elem.send_keys(Keys.BACKSPACE)
        from_elem.send_keys(from_date)

        to_elem = self.wait.until(EC.element_to_be_clickable(self._to_date_input))
        to_elem.send_keys(Keys.COMMAND if "darwin" in os.sys.platform else Keys.CONTROL, "a")
        to_elem.send_keys(Keys.BACKSPACE)
        to_elem.send_keys(to_date)

        if comment:
            try:
                comment_elem = self.wait.until(EC.element_to_be_clickable(self._comments_textarea))
                comment_elem.send_keys(comment)
            except Exception:
                pass

        self.wait.until(EC.element_to_be_clickable(self._submit_btn)).click()

    def get_toast_message(self):
        """Retrieve toast notification text."""
        toast = self.wait.until(EC.visibility_of_element_located(self._toast_message))
        return toast.text
