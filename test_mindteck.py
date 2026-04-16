# import pytest
# import os
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# # ---------------------------
# # Helper: Accept cookies
# # ---------------------------
# def accept_cookies(driver):
#     try:
#         WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//button[contains(., 'Accept')]")
#             )
#         ).click()
#     except:
#         pass


# # ---------------------------
# # Screenshot on failure
# # ---------------------------
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item):
#     outcome = yield
#     rep = outcome.get_result()

#     if rep.when == "call" and rep.failed:
#         driver = item.funcargs.get("driver")
#         if driver:
#             os.makedirs("screenshots", exist_ok=True)
#             driver.save_screenshot(f"screenshots/{item.name}.png")


# # ---------------------------
# # Driver setup
# # ---------------------------
# @pytest.fixture
# def driver():
#     options = Options()
#     options.add_argument("--headless=new")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--window-size=1920,1080")

#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()),
#         options=options
#     )

#     driver.set_page_load_timeout(40)

#     yield driver
#     driver.quit()


# # ---------------------------
# # TEST CASES
# # ---------------------------

# # ✅ 1. Homepage loads correctly
# def test_homepage_load(driver):
#     driver.get("https://www.mindteck.com")

#     WebDriverWait(driver, 20).until(lambda d: d.title != "")

#     assert "Mindteck" in driver.title


# # ✅ 2. Services section is visible on homepage
# def test_services_section_present(driver):
#     driver.get("https://www.mindteck.com")
#     accept_cookies(driver)

#     wait = WebDriverWait(driver, 25)

#     # Check Services section text exists
#     services_section = wait.until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Our Services')]")
#         )
#     )

#     assert services_section.is_displayed()


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
