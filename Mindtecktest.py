import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


# ---------- Setup & Teardown ----------
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")   # REQUIRED for Cloud
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


# ---------- Test 1: Homepage Load ----------
def test_homepage_load(driver):
    driver.get("https://www.mindteck.com")

    # Verify title contains 'Mindteck'
    assert "Mindteck" in driver.title


# ---------- Test 2: Navigation Menu ----------
def test_navigation_services(driver):
    driver.get("https://www.mindteck.com")

    # Click on Services menu
    services_menu = driver.find_element(By.LINK_TEXT, "Services")
    services_menu.click()

    # Verify URL or page content
    assert "services" in driver.current_url.lower()


# ---------- Test 3: Contact Page ----------
def test_contact_page(driver):
    driver.get("https://www.mindteck.com/contact-us/")

    # Verify heading exists
    heading = driver.find_element(By.TAG_NAME, "h1")
    assert "Contact" in heading.text


# ---------- Test 4: Form Validation ----------
def test_contact_form_validation(driver):
    driver.get("https://www.mindteck.com/contact-us/")

    # Click submit without filling form
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' or @type='button']")
    submit_button.click()

    # Check if validation appears (generic check)
    assert driver.page_source.lower().find("required") != -1


# ---------- Test 5: Footer Links ----------
def test_footer_links(driver):
    driver.get("https://www.mindteck.com")

    footer = driver.find_element(By.TAG_NAME, "footer")
    links = footer.find_elements(By.TAG_NAME, "a")

    # Ensure footer has links
    assert len(links) > 0
