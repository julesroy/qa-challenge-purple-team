import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # options.add_argument("--headless=new") # uncomment if we want to run in background (no window)
    
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()