import os
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LeavePage:
    """Page object for the Leave section of the website."""
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.apply_leave_url = "https://opensource-demo.orangehrmlive.com/web/index.php/leave/applyLeave"
        self.my_leave_url = "https://opensource-demo.orangehrmlive.com/web/index.php/leave/viewMyLeaveList"

        # card header
        self._card_header = (By.XPATH, "//h6[contains(., 'Apply Leave')]")

        # form selectors
        self._leave_type_select = (By.XPATH, "//label[text()='Leave Type']/parent::div/following-sibling::div//div[contains(@class, 'oxd-select-text')]")
        self._from_date_input = (By.XPATH, "//label[text()='From Date']/parent::div/following-sibling::div//input")
        self._to_date_input = (By.XPATH, "//label[text()='To Date']/parent::div/following-sibling::div//input")
        self._comments_textarea = (By.XPATH, "//label[text()='Comments']/parent::div/following-sibling::div//textarea")
        self._submit_btn = (By.CSS_SELECTOR, "button[type='submit']")

        # toast notification
        self._toast_message = (By.CSS_SELECTOR, ".oxd-text--toast-message, .oxd-toast-content, .oxd-toast")

    def _wait_for_spinner(self):
        """Wait for any loading spinner or form overlay to disappear."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".oxd-form-loader, .oxd-loading-spinner"))
            )
        except Exception:
            pass

    def navigate_to_apply(self):
        """Navigate to Leave > Apply and wait for the card to render."""
        self.driver.get(self.apply_leave_url)
        self.wait.until(EC.visibility_of_element_located(self._card_header))
        self._wait_for_spinner()
        time.sleep(0.5)

    def cancel_pending_leaves(self):
        """Cancel any pending leave requests in My Leave to free up dates and restore balance."""
        try:
            self.driver.get(self.my_leave_url)
            self._wait_for_spinner()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h5[contains(., 'My Leave List')]")))
            time.sleep(1)

            while True:
                cancel_btns = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Cancel']")
                if not cancel_btns:
                    break
                cancel_btns[0].click()
                time.sleep(1.5)
                self._wait_for_spinner()
        except Exception:
            pass

    @staticmethod
    def _format_date(date_str: str, placeholder: str) -> str:
        """Format an ISO/standard date string to match the input's placeholder format."""
        if not placeholder or not date_str:
            return date_str

        dt = None
        for fmt in ("%Y-%m-%d", "%Y-%d-%m", "%d-%m-%Y", "%m-%d-%Y"):
            try:
                dt = datetime.datetime.strptime(date_str, fmt)
                break
            except ValueError:
                pass

        if not dt:
            return date_str

        p = placeholder.lower().strip()
        if p == "yyyy-dd-mm":
            return f"{dt.year:04d}-{dt.day:02d}-{dt.month:02d}"
        elif p == "yyyy-mm-dd":
            return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}"
        elif p == "dd-mm-yyyy":
            return f"{dt.day:02d}-{dt.month:02d}-{dt.year:04d}"
        elif p == "mm-dd-yyyy":
            return f"{dt.month:02d}-{dt.day:02d}-{dt.year:04d}"

        return date_str

    def is_no_leave_balance_displayed(self):
        """Check if 'No Leave Types with Leave Balance' notice is shown without stale element issues."""
        self._wait_for_spinner()
        try:
            def _check_balance(d):
                body_text = d.find_element(By.TAG_NAME, "body").text
                if "No Leave Types with Leave Balance" in body_text:
                    return True
                select_elements = d.find_elements(*self._leave_type_select)
                if select_elements and select_elements[0].is_displayed():
                    return False
                return None

            result = WebDriverWait(self.driver, 6).until(_check_balance)
            return bool(result)
        except Exception:
            try:
                return "No Leave Types with Leave Balance" in self.driver.find_element(By.TAG_NAME, "body").text
            except Exception:
                return False

    def _select_first_leave_type(self):
        self._wait_for_spinner()
        dropdown = self.wait.until(EC.element_to_be_clickable(self._leave_type_select))
        try:
            dropdown.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", dropdown)
        time.sleep(0.5)
        first_option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-select-dropdown div[role='option']:not(:first-child)")))
        try:
            first_option.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", first_option)

    def apply_leave(self, from_date: str, to_date: str, comment: str = None):
        """Fill and submit leave request with automatic localization format detection."""
        self._select_first_leave_type()

        from_elem = self.wait.until(EC.element_to_be_clickable(self._from_date_input))
        to_elem = self.wait.until(EC.element_to_be_clickable(self._to_date_input))

        # Detect active date format from placeholder
        placeholder = from_elem.get_attribute("placeholder") or "yyyy-mm-dd"
        formatted_from = self._format_date(from_date, placeholder)
        formatted_to = self._format_date(to_date, placeholder)

        # Clear and input from_date
        from_elem.send_keys(Keys.CONTROL + "a")
        from_elem.send_keys(Keys.BACKSPACE)
        from_elem.send_keys(formatted_from)

        # Wait for OrangeHRM to copy From Date into To Date on blur
        from_elem.send_keys(Keys.TAB)
        self.wait.until(
            lambda _: to_elem.get_attribute("value") == formatted_from
        )

        # Clear and input to_date
        to_elem.send_keys(Keys.CONTROL + "a")
        to_elem.send_keys(Keys.BACKSPACE)
        to_elem.send_keys(formatted_to)

        # Trigger blur to let OrangeHRM recalculate balance & duration
        to_elem.send_keys(Keys.TAB)
        time.sleep(0.5)

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
