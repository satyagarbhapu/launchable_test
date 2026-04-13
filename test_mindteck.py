import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)   # 🔥 important

    yield driver
    driver.quit()


def test_homepage_load(driver):
    driver.get("https://www.mindteck.com")
    assert "Mindteck" in driver.title


def test_navigation_services(driver):
    driver.get("https://www.mindteck.com")
    driver.find_element(By.LINK_TEXT, "Services").click()
    assert "services" in driver.current_url.lower()


def test_contact_page(driver):
    driver.get("https://www.mindteck.com/contact-us/")
    heading = driver.find_element(By.TAG_NAME, "h1")
    assert "Contact" in heading.text


def test_contact_form_validation(driver):
    driver.get("https://www.mindteck.com/contact-us/")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    assert "required" in driver.page_source.lower()


def test_footer_links(driver):
    driver.get("https://www.mindteck.com")
    footer = driver.find_element(By.TAG_NAME, "footer")
    assert len(footer.find_elements(By.TAG_NAME, "a")) > 0
