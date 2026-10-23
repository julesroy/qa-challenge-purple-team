from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

        # selectors
        self._username_input = (By.NAME, "username")
        self._password_input = (By.NAME, "password")
        self._submit_button = (By.CSS_SELECTOR, "button[type='submit']")

    def open(self):
        self.driver.get(self.url)
        self.wait.until(EC.visibility_of_element_located(self._username_input))

    def login(self, username, password):
        # enter credentials with explicit wait
        user_field = self.wait.until(EC.element_to_be_clickable(self._username_input))
        user_field.clear()
        user_field.send_keys(username)

        pwd_field = self.wait.until(EC.element_to_be_clickable(self._password_input))
        pwd_field.clear()
        pwd_field.send_keys(password)

        submit_btn = self.wait.until(EC.element_to_be_clickable(self._submit_button))
        submit_btn.click()