import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver
    driver.quit()


# ✅ 1. Homepage loads
def test_homepage_load(driver):
    driver.get("https://www.mindteck.com")
    assert "mindteck" in driver.title.lower()


# ✅ 2. URL is correct
def test_homepage_url(driver):
    driver.get("https://www.mindteck.com")
    assert "mindteck.com" in driver.current_url


# ✅ 3. Page body exists
def test_body_present(driver):
    driver.get("https://www.mindteck.com")

    body = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.TAG_NAME, "body")
    )

    assert body is not None


# ✅ 4. Contact page opens
def test_contact_page_open(driver):
    driver.get("https://www.mindteck.com/contact-us/")
    assert "contact" in driver.current_url.lower()


# ✅ 5. Footer exists
def test_footer_present(driver):
    driver.get("https://www.mindteck.com")

    footer = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.TAG_NAME, "footer")
    )

    assert footer is not None
