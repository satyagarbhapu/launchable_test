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
                (By.XPATH, "//button[contains(., 'Accept')]")
            )
        ).click()
    except:
        pass


# ---------------------------
# Screenshot on failure
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
# Driver setup
# ---------------------------
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

    driver.set_page_load_timeout(40)

    yield driver
    driver.quit()


# ---------------------------
# TEST CASES
# ---------------------------

# ✅ 1. Homepage loads correctly
def test_homepage_load(driver):
    driver.get("https://www.mindteck.com")

    WebDriverWait(driver, 20).until(lambda d: d.title != "")

    assert "Mindteck" in driver.title


# ✅ 2. Services section is visible on homepage
def test_services_section_present(driver):
    driver.get("https://www.mindteck.com")
    accept_cookies(driver)

    wait = WebDriverWait(driver, 25)

    # Check Services section text exists
    services_section = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Our Services')]")
        )
    )

    assert services_section.is_displayed()


# ✅ 3. Navigate to Contact page and verify heading
def test_contact_page_heading(driver):
    driver.get("https://www.mindteck.com/contact-us/")
    accept_cookies(driver)

    wait = WebDriverWait(driver, 25)

    heading = wait.until(
        EC.presence_of_element_located((By.XPATH, "//h1 | //h2"))
    )

    assert "contact" in heading.text.lower()


# ✅ 4. Contact form should NOT submit empty (validation test)
def test_contact_form_not_submitted_empty(driver):
    driver.get("https://www.mindteck.com/contact-us/")
    accept_cookies(driver)

    wait = WebDriverWait(driver, 25)

    current_url = driver.current_url

    submit_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button | //input[@type='submit']")
        )
    )

    driver.execute_script("arguments[0].click();", submit_btn)

    # Wait and verify no navigation (validation triggered)
    WebDriverWait(driver, 5).until(lambda d: d.current_url == current_url)

    assert driver.current_url == current_url


# ✅ 5. Footer contains links
def test_footer_links_present(driver):
    driver.get("https://www.mindteck.com")
    accept_cookies(driver)

    wait = WebDriverWait(driver, 25)

    footer = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "footer"))
    )

    links = footer.find_elements(By.TAG_NAME, "a")

    assert len(links) > 0
