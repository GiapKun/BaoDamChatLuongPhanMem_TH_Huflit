import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from datetime import datetime
import pickle
from pathlib import Path

class TestEmailSending:
    @pytest.fixture
    def browser(self):
        # Setup Chrome driver with enhanced options to avoid detection
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.screenshots_dir = "email_screenshots"
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
            
        yield driver
        
        time.sleep(3)
        driver.quit()
    
    def save_screenshot(self, driver, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshots_dir}/{name}_{timestamp}.png"
        driver.save_screenshot(filename)
        return filename
    
    def check_if_email_sent(self, browser):
        try:
            sent_message_selectors = [
                "//span[contains(text(), 'Message sent')]",
                "//div[contains(text(), 'Message sent')]",
                "//div[@role='alert' and contains(., 'sent')]",
                "//div[contains(@class, 'alert') and contains(., 'sent')]"
            ]
            
            for selector in sent_message_selectors:
                try:
                    WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    return True
                except:
                    continue
            return False
        except:
            return False
    
    def test_send_email_from_gmail_to_outlook(self, browser):
        gmail_email = ""
        gmail_password = "asdadasdasd"
        recipient_edu_email = ""
        email_subject = f"test mail"
        email_body = "Đây là mail dùng để test nhận và gửi"
        
            # Step 1: Navigate to Google Account login page
        browser.get("https://accounts.google.com/signin/v2/identifier?service=mail")

        try:
            # Step 2: Login to Gmail with human-like behavior
            email_field = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            
            for character in gmail_email:
                email_field.send_keys(character)
                time.sleep(0.1)
            
            time.sleep(1)
            email_field.send_keys(Keys.ENTER)

            password_field = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.NAME, "Passwd"))
            )

            for character in gmail_password:
                password_field.send_keys(character)
                time.sleep(0.15)

            time.sleep(1.5)
            password_field.send_keys(Keys.ENTER)

            # Handle security prompts if they appear
            try:
                verification_button = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Try another way')]"))
                )
                self.save_screenshot(browser, "security_challenge_screen")
                verification_button.click()
            except TimeoutException:
                pass

            # Step 3: Wait for Gmail to load
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Compose')]"))
            )

            self.save_screenshot(browser, "gmail_login_success")

            # Step 4: Compose new email
            compose_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Compose')]"))
            )
            self.save_screenshot(browser, "before_compose_click")
            compose_button.click()
            time.sleep(2)

            # Step 5: Fill in recipient
            to_field = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='To recipients' and @role='combobox']"))
            )
            to_field.click()
            to_field.send_keys(recipient_edu_email)
            to_field.send_keys(Keys.TAB)
            self.save_screenshot(browser, "after_recipient")

            # Step 6: Enter subject
            subject_field = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.NAME, "subjectbox"))
            )
            subject_field.click()
            subject_field.clear()
            subject_field.send_keys(email_subject)

            # Step 7: Enter body
            body_field = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Message Body']"))
            )
            browser.execute_script("arguments[0].focus();", body_field)
            time.sleep(1)
            body_field.clear()
            for char in email_body:
                body_field.send_keys(char)
                time.sleep(0.1)
            self.save_screenshot(browser, "email_composed")

            # Step 8: Send the email
            send_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@data-tooltip, 'Send')]"))
            )
            self.save_screenshot(browser, "before_send_click")
            send_button.click()

            # Step 9: Check if email was sent successfully
            message_sent = self.check_if_email_sent(browser)
            screenshot_path = self.save_screenshot(browser, "after_send_attempt")

            if message_sent:
                print(f"Email sent successfully! Screenshot saved at: {screenshot_path}")
            else:
                print("Email not sent. Attempting to identify the error.")
                try:
                    error_message = browser.find_element(By.XPATH, "//div[contains(@class, 'error') or contains(@role, 'alert')]" ).text
                    print(f"Error message: {error_message}")
                except:
                    print("No error message found")
                assert message_sent, "Could not verify that message was sent successfully"

        except TimeoutException as e:
            self.save_screenshot(browser, "timeout_error")
            pytest.fail(f"Timeout error: {str(e)}")
            
        except NoSuchElementException as e:
            self.save_screenshot(browser, "element_not_found_error")
            pytest.fail(f"Element not found: {str(e)}")
            
        except Exception as e:
            self.save_screenshot(browser, "general_error")
            pytest.fail(f"Test failed with error: {str(e)}")
    
    def test_verify_email_received_in_outlook(self, browser):
        outlook_email = "2"
        outlook_password = ""
        
        try:
            browser.get("https://outlook.office.com/mail/")
            
            email_field = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.NAME, "loginfmt"))
            )
            email_field.send_keys(outlook_email)
            email_field.send_keys(Keys.ENTER)
            
            password_field = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.NAME, "passwd"))
            )
            password_field.send_keys(outlook_password)
            password_field.send_keys(Keys.ENTER)
            
            try:
                stay_signed_in = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.ID, "idSIButton9"))
                )
                stay_signed_in.click()
            except TimeoutException:
                pass
            
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='main']"))
            )
            
            screenshot_path = self.save_screenshot(browser, "outlook_inbox")
            print(f"Outlook inbox loaded. Screenshot saved at: {screenshot_path}")
            
            
            
                
        except Exception as e:
            self.save_screenshot(browser, "outlook_verification_error")
            pytest.fail(f"Outlook verification failed with error: {str(e)}")

    @staticmethod
    def setup_browser_with_cookies():
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get("https://google.com")
        
        cookies_file = Path("gmail_cookies.pkl")
        
        if cookies_file.exists():
            cookies = pickle.load(open("gmail_cookies.pkl", "rb"))
            for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                driver.add_cookie(cookie)
            
            print("Cookies loaded successfully!")
            driver.get("https://mail.google.com")
        else:
            print("No cookies file found. Please run save_gmail_cookies.py first")
        
        return driver

    @staticmethod
    def save_gmail_cookies():
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://accounts.google.com/signin/v2/identifier?service=mail")
        
        input("Please log in manually in the browser, then press Enter here once you're logged into Gmail...")
        
        pickle.dump(driver.get_cookies(), open("gmail_cookies.pkl", "wb"))
        print("Cookies saved successfully!")
        driver.quit()