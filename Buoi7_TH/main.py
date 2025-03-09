import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class TestAutomationExercise:
    @pytest.fixture
    def browser(self):
        # Setup Chrome driver
        service = Service()
        driver = webdriver.Chrome(service=service)
        # Make the window maximize
        driver.maximize_window()
        yield driver
        # Quit the browser after test
        driver.quit()
        
    def test_login_with_incorrect_credentials(self, browser):
        # 1. Launch browser - Already done in fixture
        
        # 2. Navigate to url 'http://automationexercise.com'
        browser.get("https://automationexercise.com")
        
        # 3. Verify that home page is visible successfully
        # We can check for a specific element that should be on the home page
        try:
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".shop-menu"))
            )
            print("Home page is visible successfully")
        except TimeoutException:
            pytest.fail("Home page did not load successfully")
        
        # 4. Click on 'Signup / Login' button
        signup_login_button = browser.find_element(By.CSS_SELECTOR, "a[href='/login']")
        signup_login_button.click()
        
        # 5. Verify 'Login to your account' is visible
        try:
            login_text = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[text()='Login to your account']"))
            )
            print("'Login to your account' is visible")
        except TimeoutException:
            pytest.fail("'Login to your account' text is not visible")
        
        # 6. Enter incorrect email address and password
        email_field = browser.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']")
        email_field.send_keys("incorrect_email@example.com")
        
        password_field = browser.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']")
        password_field.send_keys("incorrect_password")
        
        # 7. Click 'login' button
        login_button = browser.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']")
        login_button.click()
        
        # 8. Verify error 'Your email or password is incorrect!' is visible
        # Take a screenshot of successful login
        browser.save_screenshot("login_with_email_or_password_incorrect.png")
        try:
            error_message = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[text()='Your email or password is incorrect!']"))
            )
            print("Error message 'Your email or password is incorrect!' is visible")
        except TimeoutException:
            pytest.fail("Error message 'Your email or password is incorrect!' is not visible")