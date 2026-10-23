import json
import os
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.admin_page import AdminPage

def load_user_dataset():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "users.json")
    with open(path, "r") as f:
        return json.load(f)

# TEST-UI-10 : Multiple user creation via dataset (Data-driven testing)
@pytest.mark.parametrize("user_data", load_user_dataset())
def test_ui_10(driver, user_data):
    login_page = LoginPage(driver)
    admin_page = AdminPage(driver)
    wait = WebDriverWait(driver, 10)

    # 1. Login as Admin
    login_page.open()
    login_page.login("Admin", "admin123")
    wait.until(EC.url_contains("/dashboard/index"))

    # 2. Navigate to Add User
    admin_page.navigate_to_add_user()

    # 3. Create user using dataset record (with unique suffix to guarantee idempotency across runs)
    unique_username = f"{user_data['username']}.{int(time.time() * 1000) % 100000}"
    admin_page.create_user(
        role=user_data["role"],
        status=user_data["status"],
        username=unique_username,
        password=user_data["password"],
        employee_hint=user_data.get("employee_name", "a")
    )

    # 4. Validations
    toast = admin_page.get_toast_message()
    assert "Successfully Saved" in toast or "Success" in toast, (
        f"Expected user creation success toast for {unique_username}, got: {toast}"
    )
