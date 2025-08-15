import asyncio
from playwright.async_api import async_playwright

async def debug_after_continue():
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
            
            # Take screenshot before clicking Continue
            await page.screenshot(path="before_continue.png")
            print("📸 Screenshot before Continue: before_continue.png")
            
            # Click Continue button
            print("⏳ Clicking Continue button...")
            await page.click('#ctl00_cphBody_btnContinue')
            print("✅ Continue button clicked")
            
            # Wait for page to load
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_timeout(3000)
            
            # Take screenshot after clicking Continue
            await page.screenshot(path="after_continue.png")
            print("📸 Screenshot after Continue: after_continue.png")
            
            # Check current URL
            current_url = page.url
            print(f"Current URL after Continue: {current_url}")
            
            # Look for any elements containing "fee", "price", "cost", etc.
            print("\n🔍 Looking for fee-related elements after Continue...")
            
            # Check for the original appraisal fee element
            try:
                fee_element = await page.query_selector('#ctl00_cphBody_lblAppraisalFee')
                if fee_element:
                    is_visible = await fee_element.is_visible()
                    text_content = await fee_element.text_content()
                    print(f"  Original fee element found:")
                    print(f"    Visible: {is_visible}")
                    print(f"    Text: '{text_content}'")
                else:
                    print("  Original fee element not found")
            except Exception as e:
                print(f"  Error checking original fee element: {e}")
            
            # Look for any elements with "fee" in their ID or class
            fee_elements = await page.query_selector_all('[id*="fee"], [class*="fee"], [id*="price"], [class*="price"], [id*="cost"], [class*="cost"]')
            print(f"Found {len(fee_elements)} fee/price/cost related elements:")
            
            for i, element in enumerate(fee_elements):
                try:
                    element_id = await element.get_attribute('id')
                    element_class = await element.get_attribute('class')
                    element_text = await element.text_content()
                    is_visible = await element.is_visible()
                    
                    print(f"  Element {i+1}:")
                    print(f"    ID: {element_id}")
                    print(f"    Class: {element_class}")
                    print(f"    Text: '{element_text}'")
                    print(f"    Visible: {is_visible}")
                    print()
                except Exception as e:
                    print(f"  Element {i+1}: Error getting details - {e}")
            
            # Look for any labels or spans that might contain fee information
            print("\n🔍 Looking for labels and spans...")
            labels = await page.query_selector_all('label, span')
            for i, label in enumerate(labels[:20]):  # Check first 20
                try:
                    label_text = await label.text_content()
                    if any(term in label_text.lower() for term in ['fee', 'price', 'cost', 'amount', '$']):
                        label_id = await label.get_attribute('id')
                        label_class = await label.get_attribute('class')
                        print(f"  Label {i+1}: '{label_text}' (ID: {label_id}, Class: {label_class})")
                except:
                    pass
            
            # Check if we're on a different page now
            print("\n🔍 Checking if we're on a different page...")
            page_title = await page.title()
            print(f"Page title: {page_title}")
            
            # Look for any form elements that might be on the new page
            forms = await page.query_selector_all('form')
            print(f"Found {len(forms)} forms on the page")
            
            # Keep browser open for manual inspection
            print("\n🔍 Browser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_after_continue())
