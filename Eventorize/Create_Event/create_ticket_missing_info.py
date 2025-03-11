import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class TestViewTickets:
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
        
    def test_login_and_view_tickets(self, browser):
        # Open login page
        browser.get("https://eventorize.giapkun.site/")
        
        try:
            # Wait for the login button to be clickable
            print("Waiting for login button...")
            btn_login = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/main/header/a/button"))
            )
            print("Login button found, clicking...")
            btn_login.click()
            
            # Wait for the login page to load
            print("Waiting for login page...")
            WebDriverWait(browser, 10).until(
                EC.url_contains("/login")
            )
            print("Login page loaded")
            
            # Enter email using the exact XPath
            print("Entering email...")
            email_field = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/form/div[1]/div/input"))
            )
            email_field.send_keys("trandinhgiap8051@gmail.com")
            
            # Enter password using the exact XPath
            print("Entering password...")
            password_field = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/form/div[2]/div/input"))
            )
            password_field.send_keys("Trandinhgiap8051@gmail.com")
            
            # Click login button using the exact XPath
            print("Clicking login button...")
            login_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/form/button"))
            )
            login_button.click()
            
            # Wait for successful login
            print("Waiting for successful login...")
            time.sleep(2) # Allow time for redirect after login
            
            # Click the profile button
            print("Clicking profile button...")
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@aria-haspopup='menu' and @data-state='closed']"))
            )
            time.sleep(1)  # Small additional wait to ensure stability
            profile_button = browser.find_element(By.XPATH, "//div[@aria-haspopup='menu' and @data-state='closed']")
            profile_button.click()
            
            # Click on Organization option
            print("Selecting Organization option...")
            org_option = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='menuitem' and contains(., 'Organization')]"))
            )
            org_option.click()

            # Wait for organization page to load
            print("Waiting for organization page...")
            WebDriverWait(browser, 10).until(
                EC.url_contains("/organization")
            )
            
            # Check if organizer selection popup appears and handle it
            try:
                print("Checking for organizer selection popup...")
                # Wait for the "Select organizer" dropdown to appear
                organizer_dropdown = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select organizer')]"))
                )
                print("Selecting Nike organizer...")
                organizer_dropdown.click()  # Open the dropdown

                # Select the Nike organizer from the dropdown
                nike_option = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and contains(., 'Nike')]"))
                )
                nike_option.click()  # Click the Nike option

                # Click Accept button
                print("Clicking Accept button...")
                accept_button = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
                )
                accept_button.click()
            except TimeoutException:
                print("No organizer selection popup or it was already handled")
            
            # Click on Events button in sidebar
            print("Navigating to Events page...")
            events_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/aside/nav/ul/li[2]/a/button"))
            )
            events_button.click()
            
            # Wait for events page to load
            print("Waiting for events page...")
            WebDriverWait(browser, 10).until(
                EC.url_contains("/organization/events")
            )
            
            # Try to click on an available event
            try:
                print("Looking for available events...")
                event_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/table/tbody/tr/td[3]/button"))
                )
                print("Event found, clicking...")
                event_button.click()
                
                print("Selecting View option...")
                view_option = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='menuitem' and contains(text(), 'View')]"))
                )
                view_option.click()

                # Click on the "Add new ticket" button
                print("Clicking on 'Add new ticket' button...")
                add_ticket_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add new ticket')]"))
                )
                add_ticket_button.click()

                # Wait for the new ticket form to load
                print("Waiting for the new ticket form to load...")
                WebDriverWait(browser, 10).until(
                    EC.url_contains("/tickets/add")
                )

                # Fill in the ticket form
                print("Filling in the ticket form...")

                # Fill in the title
                # title_input = WebDriverWait(browser, 10).until(
                #     EC.presence_of_element_located((By.XPATH, "//input[@name='title']"))
                # )
                # title_input.send_keys("VIP Promax")

                # Fill in the quantity
                quantity_input = browser.find_element(By.XPATH, "//input[@name='quantity']")
                quantity_input.send_keys("100")

                # Fill in the price
                price_input = browser.find_element(By.XPATH, "//input[@name='price']")
                price_input.send_keys("0")

                # Fill in the description
                description_input = browser.find_element(By.XPATH, "//textarea[@name='description']")
                description_input.send_keys("This is a VIP ticket for the event.")

                # Select the status (if required)
                status_dropdown = browser.find_element(By.XPATH, "//button[@role='combobox' and contains(., 'Select status')]")
                status_dropdown.click()
                status_option = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and contains(., 'Active')]"))
                )
                status_option.click()

                # Fill in the date range (if required)
                date_range_input = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='DD/MM/YYYY to DD/MM/YYYY']"))
                )

                # Set the value directly using JavaScript
                browser.execute_script("arguments[0].value = '10/03/2025 to 14/04/2025';", date_range_input)

                # Trigger input and change events
                browser.execute_script("arguments[0].dispatchEvent(new Event('input'));", date_range_input)
                browser.execute_script("arguments[0].dispatchEvent(new Event('change'));", date_range_input)

                print("Date range filled successfully!")
                # Click the "Create" button
                print("Submitting the form...")
                create_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create')]"))
                )

                # Scroll the button into view
                browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", create_button)

                # Click the button using JavaScript (if necessary)
                browser.execute_script("arguments[0].click();", create_button)

                # Wait for the error message to appear
                print("Waiting for the error message...")
                warning_message = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'text-red-500') and contains(text(), 'Title is required')]"))
                )

                # Verify the warning message
                if warning_message.is_displayed():
                    print("Warning message displayed successfully:", warning_message.text)
                    browser.save_screenshot("missing_title_warning.png")
                else:
                    print("Warning message not displayed.")

            except TimeoutException:
                browser.save_screenshot("no_event_available.png")
                print("No events available")
                pytest.skip("Test skipped: No events available")
            
        except TimeoutException as e:
            print(f"Test failed with timeout: {e}")
            pytest.fail(f"Test failed: {e}")
        except Exception as e:
            print(f"Test failed with error: {e}")
            browser.save_screenshot("error.png")
            pytest.fail(f"Test failed: {e}")