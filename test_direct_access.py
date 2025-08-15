import asyncio
from playwright.async_api import async_playwright

async def test_direct_access():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("Testing direct access to AddAppraisal.aspx...")
            await page.goto('https://nadlanvaluation.spurams.com/AddAppraisal.aspx')
            await page.wait_for_load_state("networkidle")
            
            # Check if we're redirected to login or if we can access the form
            current_url = page.url
            print(f"Current URL: {current_url}")
            
            # Check if the form elements are present
            try:
                await page.wait_for_selector('#ctl00_cphBody_drpTransactionType', timeout=5000)
                print("✅ SUCCESS: Form elements found - direct access works!")
                return True
            except:
                print("❌ FAILED: Form elements not found - login required")
                return False
                
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_direct_access())
