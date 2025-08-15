import asyncio
from playwright.async_api import async_playwright

async def simple_fee_test():
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
            
            # Wait a bit
            await page.wait_for_timeout(3000)
            
            # Check for the specific appraisal fee element
            print("\n🔍 Checking for appraisal fee element...")
            fee_element = await page.query_selector('#ctl00_cphBody_lblAppraisalFee')
            
            if fee_element:
                print("✅ Appraisal fee element found!")
                text_content = await fee_element.text_content()
                is_visible = await fee_element.is_visible()
                print(f"  Text: '{text_content}'")
                print(f"  Visible: {is_visible}")
                
                if text_content and text_content.strip():
                    print(f"✅ SUCCESS: Found appraisal fee: {text_content}")
                else:
                    print("⚠️ Element exists but has no text content")
            else:
                print("❌ Appraisal fee element not found")
            
            # Take a screenshot
            await page.screenshot(path="simple_fee_test.png")
            print("📸 Screenshot saved as simple_fee_test.png")
            
            # Keep browser open for manual inspection
            print("\n🔍 Browser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(simple_fee_test())
