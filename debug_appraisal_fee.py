import asyncio
import json
import sys
from playwright.async_api import async_playwright

async def debug_appraisal_fee():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        
        try:
            # Navigate and login
            print("🚀 Navigating to AddAppraisal.aspx...")
            await page.goto('https://nadlanvaluation.spurams.com/AddAppraisal.aspx')
            await page.wait_for_load_state("domcontentloaded")
            
            # Login
            await page.fill('#ctl00_cphBody_Login1_UserName', 'AaronK')
            await page.fill('#ctl00_cphBody_Login1_Password', 'berlinchildhood$')
            await page.click('#ctl00_cphBody_Login1_LoginButton')
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_timeout(2000)
            
            # Wait for form
            await page.wait_for_selector('#ctl00_cphBody_drpTransactionType', timeout=5000)
            print("✅ Form loaded")
            
            # Fill all the fields
            print("📝 Filling form fields...")
            
            # Transaction Type
            await page.select_option('#ctl00_cphBody_drpTransactionType', '1')
            print("✅ Transaction Type")
            await page.wait_for_timeout(500)
            
            # Loan Type
            await page.select_option('#ctl00_cphBody_drpLoanType', '5')
            print("✅ Loan Type")
            await page.wait_for_timeout(500)
            
            # Property Type
            await page.select_option('#ctl00_cphBody_drpPropertyType', '13')
            print("✅ Property Type")
            await page.wait_for_timeout(500)
            
            # Property Address
            await page.fill('#ctl00_cphBody_txtPropertyAddress', '15 Burr Avenue')
            print("✅ Property Address")
            await page.wait_for_timeout(500)
            
            # Property City
            await page.fill('#ctl00_cphBody_txtPropertyCity', 'Marlboro Township')
            print("✅ Property City")
            await page.wait_for_timeout(500)
            
            # Property State
            await page.select_option('#ctl00_cphBody_drpPropertyState', 'NJ')
            print("✅ Property State")
            await page.wait_for_timeout(500)
            
            # Property Zip
            await page.fill('#ctl00_cphBody_txtPropertyZip', '07751')
            print("✅ Property Zip")
            await page.wait_for_timeout(1000)
            
            # Occupancy Type
            await page.select_option('#ctl00_cphBody_drpOccupiedBy', 'Investment')
            print("✅ Occupancy Type")
            await page.wait_for_timeout(500)
            
            # Product/Appraisal Type
            await page.select_option('#ctl00_cphBody_drpAppraisalType', '59')
            print("✅ Product/Appraisal Type")
            await page.wait_for_timeout(500)
            
            print("✅ All fields filled!")
            
            # Wait and look for buttons
            await page.wait_for_timeout(3000)
            
            # Look for all buttons on the page
            print("🔍 Looking for buttons on the page...")
            buttons = await page.query_selector_all('button, input[type="submit"], input[type="button"]')
            print(f"Found {len(buttons)} buttons:")
            
            for i, button in enumerate(buttons):
                try:
                    text = await button.text_content()
                    value = await button.get_attribute('value')
                    id_attr = await button.get_attribute('id')
                    class_attr = await button.get_attribute('class')
                    print(f"  Button {i+1}: text='{text}', value='{value}', id='{id_attr}', class='{class_attr}'")
                except:
                    print(f"  Button {i+1}: [error reading attributes]")
            
            # Look for appraisal fee element
            print("🔍 Looking for appraisal fee element...")
            try:
                fee_element = await page.wait_for_selector('#ctl00_cphBody_lblAppraisalFee', timeout=2000)
                if fee_element:
                    fee_text = await fee_element.text_content()
                    print(f"✅ Found appraisal fee: {fee_text}")
                else:
                    print("❌ Appraisal fee element not found")
            except:
                print("❌ Appraisal fee element not found")
            
            # Look for any elements containing "fee" or "price"
            print("🔍 Looking for any fee/price related elements...")
            fee_elements = await page.query_selector_all('[id*="fee"], [id*="price"], [class*="fee"], [class*="price"]')
            print(f"Found {len(fee_elements)} fee/price related elements:")
            
            for i, element in enumerate(fee_elements):
                try:
                    text = await element.text_content()
                    id_attr = await element.get_attribute('id')
                    class_attr = await element.get_attribute('class')
                    print(f"  Element {i+1}: text='{text}', id='{id_attr}', class='{class_attr}'")
                except:
                    print(f"  Element {i+1}: [error reading attributes]")
            
            # Take a screenshot
            await page.screenshot(path='debug_form_filled.png', full_page=True)
            print("📸 Screenshot saved as debug_form_filled.png")
            
            # Wait for user to see the page
            print("⏳ Waiting 10 seconds for you to see the page...")
            await page.wait_for_timeout(10000)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_appraisal_fee())
