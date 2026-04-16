import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------
# Helper: Accept cookies
# ---------------------------
def accept_cookies(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Accept')]")
            )
        ).click()
    except:
        pass


# ---------------------------
# Capture screenshot on failure
# ---------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(f"screenshots/{item.name}.png")


# ---------------------------
# WebDriver Fixture
# ---------------------------
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.set_page_load_timeout(30)

    yield driver
    driver.quit()


# ---------------------------
# Tests
# ---------------------------
def test_homepage_load(driver):
    driver.get("https://www.mindteck.com")
    assert "Mindteck" in driver.title


def test_navigation_services(driver):
    driver.get("https://www.mindteck.com")

    accept_cookies(driver)

    wait = WebDriverWait(driver, 20)

    services_link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Services"))
    )
    services_link.click()

    wait.until(EC.url_contains("services"))

    assert "services" in driver.current_url.lower()


def test_contact_page(driver):
    driver.get("https://www.mindteck.com/contact-us/")

    accept_cookies(driver)

    wait = WebDriverWait(driver, 20)

    heading = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )

    assert "Contact" in heading.text


def test_contact_form_validation(driver):
    driver.get("https://www.mindteck.com/contact-us/")

    accept_cookies(driver)

    wait = WebDriverWait(driver, 20)

    submit_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit'] | //input[@type='submit']")
        )
    )
    submit_btn.click()

    wait.until(lambda d: "required" in d.page_source.lower())

    assert "required" in driver.page_source.lower()


def test_footer_links(driver):
    driver.get("https://www.mindteck.com")

    accept_cookies(driver)

    wait = WebDriverWait(driver, 20)

    footer = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "footer"))
    )

    links = footer.find_elements(By.TAG_NAME, "a")

    assert len(links) > 0
