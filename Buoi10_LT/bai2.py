import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class TestHuflit:
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
        
    def test_login_with_office365(self, browser):
        # Open login page
        browser.get("https://courses.huflit.edu.vn")
        
        try:
            # Wait for the Office 365 login button to be clickable
            print("Waiting for Office 365 button...")
            office365_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/header[1]/div/div/div[2]/div/div[1]/div/div[1]/a"))
            )
            
            # Click the Office 365 login button
            print("Clicking Office 365 button...")
            office365_button.click()
            
            # Wait for redirect to Microsoft login page
            print("Waiting for redirect to Microsoft login page...")
            WebDriverWait(browser, 15).until(
                EC.url_contains("login.microsoftonline.com")
            )
            
            # Wait for email field and make sure it's fully loaded
            print("Waiting for email field...")
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.ID, "i0116"))
            )
            
            # Give extra time for the page to fully load
            time.sleep(2)
            
            # Enter email
            print("Entering email...")
            email_input = browser.find_element(By.ID, "i0116")
            email_input.clear()  # Clear any existing text
            email_input.send_keys("Nhap tai khoan vao day")  # Replace with actual email
            
            # Wait for the Next button to be clickable
            print("Waiting for Next button...")
            next_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "idSIButton9"))
            )
            
            # Click Next
            print("Clicking Next button...")
            next_button.click()
            
            # Important: Wait 5 seconds between email and password as specified
            print("Waiting 5 seconds...")
            time.sleep(5)
            
            # Wait for password field to be visible and interactive
            print("Waiting for password field...")
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.ID, "i0118"))
            )
            
            # Extra delay to ensure the password field is ready
            time.sleep(1)
            
            # Enter password
            print("Entering password...")
            password_input = browser.find_element(By.ID, "i0118")
            password_input.clear()  # Clear any existing text
            password_input.send_keys("Nhap mat khau vao day")  # Replace with actual password
            
            # Wait for Sign in button to be clickable
            print("Waiting for Sign in button...")
            sign_in_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "idSIButton9"))
            )
            
            # Click Sign in
            print("Clicking Sign in button...")
            sign_in_button.click()
            
            # If "Stay signed in?" page appears
            try:
                print("Checking for 'Stay signed in' prompt...")
                stay_signed_in = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.ID, "idSIButton9"))
                )
                print("Clicking 'Yes' on Stay signed in prompt...")
                stay_signed_in.click()
            except TimeoutException:
                # No "Stay signed in?" prompt appeared, continue
                print("No 'Stay signed in' prompt appeared.")
            
            # Wait for successful login and redirect back to the portal
            print("Waiting for redirect to HUFLIT portal...")
            WebDriverWait(browser, 30).until(
                EC.url_contains("courses.huflit.edu.vn/my")
            )
            
            print("Successfully logged in!")
            
            # Take a screenshot of successful login
            browser.save_screenshot("login_success.png")

  
            # Find and click on the specific course
            print("Looking for the Software Quality Assurance course...")
            course_element = WebDriverWait(browser, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '242123053410-Bảo đảm chất lượng phần mềm')]"))
            )
            
            # Click on the course
            print("Clicking on the course...")
            course_element.click()
            
            # Wait for the course page to load
            print("Waiting for course page to load...")
            WebDriverWait(browser, 20).until(
                EC.url_contains("course/view.php")
            )
            
            print("Successfully navigated to the course page!")
            
            # Take a screenshot of the course page
            browser.save_screenshot("course_page.png")
            
        except Exception as e:
            # Take a screenshot to debug failures
            browser.save_screenshot("login_error.png")
            print(f"Login failed: {str(e)}")
            raise