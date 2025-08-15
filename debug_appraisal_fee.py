import asyncio
import json
import sys
from playwright.async_api import async_playwright

async def debug_appraisal_fee():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("🚀 Navigating to AddAppraisal.aspx...")
            await page.goto('https://nadlanvaluation.spurams.com/AddAppraisal.aspx')
            await page.wait_for_load_state("domcontentloaded")
            
            # Login
            await page.fill('#ctl00_cphBody_Login1_UserName', 'AaronK')
            await page.fill('#ctl00_cphBody_Login1_Password', 'berlinchildhood$')
            await page.click('#ctl00_cphBody_Login1_LoginButton')
            await page.wait_for_load_state("domcontentloaded")
            
            # Wait for form to load
            await page.wait_for_selector('#ctl00_cphBody_drpTransactionType', timeout=5000)
            print("✅ Form loaded successfully")
            
            # Fill the form with test data
            await page.select_option('#ctl00_cphBody_drpTransactionType', '1')  # Purchase
            await page.select_option('#ctl00_cphBody_drpPropertyType', '13')  # Single Family
            await page.fill('#ctl00_cphBody_txtPropertyAddress', '15 Burr Avenue')
            await page.fill('#ctl00_cphBody_txtPropertyCity', 'Marlboro Township')
            await page.select_option('#ctl00_cphBody_drpPropertyState', 'NJ')
            await page.fill('#ctl00_cphBody_txtPropertyZip', '07751')
            await page.select_option('#ctl00_cphBody_drpOccupiedBy', 'Investment')
            await page.select_option('#ctl00_cphBody_drpAppraisalType', '59')
            
            print("✅ Form filled successfully")
            
            # Look for any buttons that might trigger calculation
            print("\n🔍 Looking for buttons on the page...")
            buttons = await page.query_selector_all('input[type="button"], input[type="submit"], button')
            print(f"Found {len(buttons)} buttons:")
            
            for i, button in enumerate(buttons):
                try:
                    button_text = await button.text_content()
                    button_type = await button.get_attribute('type')
                    button_id = await button.get_attribute('id')
                    button_class = await button.get_attribute('class')
                    button_value = await button.get_attribute('value')
                    
                    print(f"  Button {i+1}:")
                    print(f"    Text: {button_text}")
                    print(f"    Type: {button_type}")
                    print(f"    ID: {button_id}")
                    print(f"    Class: {button_class}")
                    print(f"    Value: {button_value}")
                    print()
                except Exception as e:
                    print(f"  Button {i+1}: Error getting details - {e}")
            
            # Look for any elements that might contain "calculate", "submit", "fee", etc.
            print("\n🔍 Looking for calculation-related elements...")
            page_content = await page.content()
            
            # Check for common calculation-related terms
            calculation_terms = ['calculate', 'submit', 'fee', 'price', 'cost', 'estimate']
            for term in calculation_terms:
                if term.lower() in page_content.lower():
                    print(f"  Found '{term}' in page content")
            
            # Check if appraisal fee element exists but is hidden
            print("\n🔍 Checking appraisal fee element...")
            try:
                fee_element = await page.query_selector('#ctl00_cphBody_lblAppraisalFee')
                if fee_element:
                    is_visible = await fee_element.is_visible()
                    text_content = await fee_element.text_content()
                    print(f"  Appraisal fee element found:")
                    print(f"    Visible: {is_visible}")
                    print(f"    Text: '{text_content}'")
                    print(f"    Display style: {await fee_element.evaluate('el => getComputedStyle(el).display')}")
                else:
                    print("  Appraisal fee element not found")
            except Exception as e:
                print(f"  Error checking fee element: {e}")
            
            # Wait a bit and check again
            print("\n⏳ Waiting 5 seconds and checking again...")
            await page.wait_for_timeout(5000)
            
            try:
                fee_element = await page.query_selector('#ctl00_cphBody_lblAppraisalFee')
                if fee_element:
                    is_visible = await fee_element.is_visible()
                    text_content = await fee_element.text_content()
                    print(f"  After waiting - Appraisal fee element:")
                    print(f"    Visible: {is_visible}")
                    print(f"    Text: '{text_content}'")
                else:
                    print("  After waiting - Appraisal fee element still not found")
            except Exception as e:
                print(f"  Error checking fee element after waiting: {e}")
            
            # Take a screenshot for debugging
            await page.screenshot(path="debug_form_filled.png")
            print("📸 Screenshot saved as debug_form_filled.png")
            
            # Keep browser open for manual inspection
            print("\n🔍 Browser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_appraisal_fee())
