import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
    
    # def test_login_elements(self, browser):
    #     # Open login page
    #     browser.get("https://portal.huflit.edu.vn/Login")
        
    #     try:
    #         # Check logo first
    #         logo = WebDriverWait(browser, 10).until(
    #             EC.presence_of_element_located((By.ID, "logo"))
    #         )
    #         assert logo.get_attribute("src").endswith("/Content/logo/logologinhuflit.png"), "Logo source is incorrect"
    #         assert logo.get_attribute("width") == "250", "Logo width is not 250px"
    #         print("✓ Logo verification passed")

            # # Check username textbox
            # username_box = browser.find_element(By.NAME, "txtTaiKhoan")
            # assert username_box.get_attribute("placeholder") == "Tên đăng nhập", "Username placeholder is incorrect"
            # assert username_box.get_attribute("class") == "form-control", "Username class is incorrect"
            # print("✓ Username textbox verification passed")

            # # Check password textbox
            # password_box = browser.find_element(By.ID, "txtMatKhau")
            # assert password_box.get_attribute("type") == "password", "Password type is incorrect"
            # assert password_box.get_attribute("placeholder") == "Mật khẩu", "Password placeholder is incorrect"
            # assert password_box.get_attribute("class") == "form-control", "Password class is incorrect"
            # print("✓ Password textbox verification passed")

    #         # Check login button
    #         login_button = browser.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Đăng nhập']")
    #         assert login_button.get_attribute("class") == "btn btn-primary btn-block", "Button class is incorrect"
    #         assert login_button.get_attribute("onclick") == "ValidateUser()", "Button onclick function is incorrect"
    #         print("✓ Login button verification passed")

    #     except (TimeoutException, NoSuchElementException) as e:
    #         raise Exception(f"Element not found: {str(e)}")
    #     except AssertionError as e:
    #         raise Exception(f"Verification failed: {str(e)}")
        
    # def test_check_text_content(self, browser):
    #     browser.get("https://portal.huflit.edu.vn/Login")
        
    #     try:
    #         # First wait for parent element
    #         loginbox = WebDriverWait(browser, 30).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, "loginbox-social"))
    #         )
            
    #         # Find school name using relative XPath within loginbox
    #         school_text = loginbox.find_element(By.XPATH, ".//div/span")
    #         actual_school_text = browser.execute_script("return arguments[0].textContent;", school_text).strip()
    #         print(f"School text found: '{actual_school_text}'")
            
    #         expected_school_text = "TRƯỜNG ĐẠI HỌC NGOẠI NGỮ - TIN HỌC TP. HỒ CHÍ MINH (HUFLIT)"
    #         assert expected_school_text in actual_school_text, f"School name text is incorrect. Expected: '{expected_school_text}', Found: '{actual_school_text}'"
    #         print("✓ School name text verification passed")

    #         # Find portal title using class name within loginbox
    #         portal_title = loginbox.find_element(By.CLASS_NAME, "social-title")
    #         actual_portal_text = browser.execute_script("return arguments[0].textContent;", portal_title).strip()
    #         print(f"Portal text found: '{actual_portal_text}'")
            
    #         expected_portal_text = "Cổng thông tin đào tạo"
    #         assert actual_portal_text == expected_portal_text, f"Portal title text is incorrect. Expected: '{expected_portal_text}', Found: '{actual_portal_text}'"
    #         print("✓ Portal title verification passed")
            
    #     except (TimeoutException, NoSuchElementException) as e:
    #         raise Exception(f"Element not found: {str(e)}")
    #     except AssertionError as e:
    #         raise Exception(f"Verification failed: {str(e)}")

    # def test_check_text_and_style(self, browser):
    #     browser.get("https://portal.huflit.edu.vn/Login")
        
    #     try:
    #         # First wait for parent element
    #         loginbox = WebDriverWait(browser, 30).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, "loginbox-social"))
    #         )
            
    #         # Find the div containing the span (to check style)
    #         school_div = loginbox.find_element(By.XPATH, ".//div[span[contains(text(), 'TRƯỜNG ĐẠI HỌC')]]")
            
    #         # Get computed styles using JavaScript
    #         style_script = """
    #             let element = arguments[0];
    #             let computedStyle = window.getComputedStyle(element);
    #             return {
    #                 fontWeight: computedStyle.fontWeight,
    #                 style: element.getAttribute('style')
    #             };
    #         """
    #         styles = browser.execute_script(style_script, school_div)
            
    #         # Print found styles for debugging
    #         print(f"Found styles: {styles}")
            
    #         # Check the exact style attribute
    #         expected_style = "margin-top: 1px; font-weight: bold; color: #183C69;"
    #         actual_style = styles['style']
    #         assert expected_style == actual_style, f"Style attribute is incorrect. Expected: '{expected_style}', Found: '{actual_style}'"
    #         print("✓ Style attribute verification passed")
            
    #         # Double check that font-weight is actually bold
    #         assert styles['fontWeight'] in ['bold', '700'], f"Text is not bold. Found font-weight: {styles['fontWeight']}"
    #         print("✓ Font weight verification passed")
            
    #         # Check text content
    #         school_text = school_div.find_element(By.TAG_NAME, "span")
    #         actual_text = browser.execute_script("return arguments[0].textContent;", school_text).strip()
    #         expected_text = "TRƯỜNG ĐẠI HỌC NGOẠI NGỮ - TIN HỌC TP. HỒ CHÍ MINH (HUFLIT)"
            
    #         assert actual_text == expected_text, f"Text content is incorrect. Expected: '{expected_text}', Found: '{actual_text}'"
    #         print("✓ Text content verification passed")
            
    #     except (TimeoutException, NoSuchElementException) as e:
    #         raise Exception(f"Element not found: {str(e)}")
    #     except AssertionError as e:
    #         raise Exception(f"Verification failed: {str(e)}")

    def test_compare_textbox_widths(self, browser):
        browser.get("https://portal.huflit.edu.vn/Login")
        
        try:
            # Wait for and find both textboxes
            username_box = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.NAME, "txtTaiKhoan"))
            )
            password_box = WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.ID, "txtMatKhau"))
            )
            
            # Get widths using JavaScript
            width_script = "return window.getComputedStyle(arguments[0]).width"
            username_width = browser.execute_script(width_script, username_box)
            password_width = browser.execute_script(width_script, password_box)
            
            # Print widths for debugging
            print(f"Username textbox width: {username_width}")
            print(f"Password textbox width: {password_width}")
            
            # Compare widths
            assert username_width == password_width, (
                f"Textbox widths are not equal.\n"
                f"Username textbox: {username_width}\n"
                f"Password textbox: {password_width}"
            )
            print("✓ Username and password textboxes have equal widths")
            
        except TimeoutException:
            raise Exception("Failed to find textboxes within timeout period")
        except AssertionError as e:
            raise Exception(f"Width comparison failed: {str(e)}")