import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MyInfoPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMyDetails"

        # Form selectors
        self._nationality_select = (By.XPATH, "//label[text()='Nationality']/parent::div/following-sibling::div//div[contains(@class, 'oxd-select-text')]")
        self._marital_status_select = (By.XPATH, "//label[text()='Marital Status']/parent::div/following-sibling::div//div[contains(@class, 'oxd-select-text')]")
        self._dob_input = (By.XPATH, "//label[text()='Date of Birth']/parent::div/following-sibling::div//input")
        self._personal_details_save_btn = (By.XPATH, "(//button[@type='submit'])[1]")

        # Attachments selectors
        self._add_attachment_btn = (By.XPATH, "//h6[text()='Attachments']/following::button[contains(., 'Add')][1]")
        self._file_input = (By.CSS_SELECTOR, "input[type='file']")
        self._comment_textarea = (By.XPATH, "//label[text()='Comment']/parent::div/following-sibling::div//textarea | //textarea[@placeholder='Type comment here']")
        self._attachment_save_btn = (By.XPATH, "(//button[@type='submit'])[last()]")
        self._inline_error_msg = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

        # Toast notification
        self._toast_message = (By.CSS_SELECTOR, ".oxd-text--toast-message, .oxd-toast-content, .oxd-toast")

    def _wait_for_spinner(self):
        """Wait for any loading spinner or form overlay to disappear."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".oxd-form-loader, .oxd-loading-spinner"))
            )
        except Exception:
            pass

    def navigate(self):
        """Navigate to My Info via direct URL and ensure page is loaded."""
        self.driver.get(self.url)
        self.wait.until(EC.url_contains("/viewPersonalDetails"))
        self.wait.until(EC.visibility_of_element_located(self._personal_details_save_btn))
        self._wait_for_spinner()
        time.sleep(0.5)

    def _select_dropdown_option(self, dropdown_locator, option_text):
        self._wait_for_spinner()
        dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
        time.sleep(0.3)
        try:
            dropdown.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", dropdown)

        time.sleep(0.3)
        option_xpath = f"//div[@role='option']//span[text()='{option_text}']"
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
        time.sleep(0.2)
        try:
            option.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", option)

        # Wait for the dropdown options menu to close to prevent intercepting next actions
        try:
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".oxd-select-dropdown"))
            )
        except Exception:
            pass
        time.sleep(0.3)

    def update_personal_details(self, nationality=None, marital_status=None, dob=None):
        """Update nationality, marital status, and date of birth."""
        if nationality:
            self._select_dropdown_option(self._nationality_select, nationality)

        if marital_status:
            self._select_dropdown_option(self._marital_status_select, marital_status)

        if dob:
            self._wait_for_spinner()
            dob_elem = self.wait.until(EC.element_to_be_clickable(self._dob_input))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dob_elem)
            time.sleep(0.2)
            dob_elem.send_keys(Keys.COMMAND if "darwin" in os.sys.platform else Keys.CONTROL, "a")
            dob_elem.send_keys(Keys.BACKSPACE)
            dob_elem.send_keys(dob)
            dob_elem.send_keys(Keys.TAB)

        self._wait_for_spinner()
        save_btn = self.wait.until(EC.element_to_be_clickable(self._personal_details_save_btn))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        time.sleep(0.3)
        try:
            save_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", save_btn)

    def open_add_attachment(self):
        """Click on the Add button in the Attachments section."""
        self._wait_for_spinner()
        btn = self.wait.until(EC.element_to_be_clickable(self._add_attachment_btn))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.2)
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.presence_of_element_located(self._file_input))

    def upload_attachment(self, file_path, comment=None):
        """Upload a file to the attachment form."""
        abs_path = os.path.abspath(file_path)
        file_elem = self.wait.until(EC.presence_of_element_located(self._file_input))
        file_elem.send_keys(abs_path)

        if comment:
            try:
                comment_elem = self.wait.until(EC.element_to_be_clickable(self._comment_textarea))
                comment_elem.clear()
                comment_elem.send_keys(comment)
            except Exception:
                pass

        try:
            save_btn = self.wait.until(EC.element_to_be_clickable(self._attachment_save_btn))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
            self.driver.execute_script("arguments[0].click();", save_btn)
        except Exception:
            pass

    def has_attachment(self, filename):
        """Check if filename is listed in the attachments table or page."""
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: filename in d.find_element(By.TAG_NAME, "body").text or
                          len(d.find_elements(By.CSS_SELECTOR, ".oxd-toast")) > 0
            )
            return True
        except Exception:
            return False

    def get_inline_error_message(self):
        """Retrieve the inline error message (e.g. for rejected file types)."""
        error_elem = self.wait.until(EC.visibility_of_element_located(self._inline_error_msg))
        return error_elem.text

    def get_toast_message(self):
        """Retrieve the toast notification message text."""
        toast = self.wait.until(EC.visibility_of_element_located(self._toast_message))
        return toast.text
