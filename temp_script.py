
import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=false)
        page = await browser.new_page()
        
        try:
            # Navigate to Nadlan valuation login page
            await page.goto("https://nadlanvaluation.spurams.com/login.aspx")
            
            # Wait for page to load
            await page.wait_for_load_state("networkidle")
            
            # Wait additional time if specified
            if 5000 > 0:
                await page.wait_for_timeout(5000)
            
            # Fill in username if provided
            username = TestUser123  # Default test value
            if username:
                try:
                    # Wait for username field to be available
                    await page.wait_for_selector('#ctl00_cphBody_Login1_UserName', timeout=5000)
                    
                    # Fill in the username
                    await page.fill('#ctl00_cphBody_Login1_UserName', username)
                    print(f"Filled username field with: {username}")
                    
                    # Wait a moment for the input to register
                    await page.wait_for_timeout(1000)
                    
                except Exception as e:
                    print(f"Error filling username: {e}")
            
            # Take a screenshot
            screenshot_path = "nadlan_screenshot.png"
            await page.screenshot(path=screenshot_path)
            
            # Get page title
            title = await page.title()
            
            # Check if login form exists
            login_form = await page.query_selector('form')
            has_login_form = login_form is not None
            
            # Get form fields if they exist
            form_fields = []
            if has_login_form:
                inputs = await page.query_selector_all('input')
                for input_elem in inputs:
                    input_type = await input_elem.get_attribute('type')
                    input_name = await input_elem.get_attribute('name')
                    input_id = await input_elem.get_attribute('id')
                    form_fields.append({
                        "type": input_type,
                        "name": input_name,
                        "id": input_id
                    })
            
            result = {
                "title": title,
                "url": "https://nadlanvaluation.spurams.com/login.aspx",
                "screenshot_path": screenshot_path,
                "has_login_form": has_login_form,
                "form_fields": form_fields,
                "variables_processed": {"headless": false, "username": "TestUser123"}
            }
            
            print(json.dumps(result))
            
        except Exception as e:
            print(f"Error: {e}")
            result = {"error": str(e)}
            print(json.dumps(result))
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

