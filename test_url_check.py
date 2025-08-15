import asyncio
import json
from playwright.async_api import async_playwright

async def test_url_after_login():
    variables = {
        'username': 'AaronK',
        'password': 'berlinchildhood$',
        'headless': False
    }
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("1. Navigating to AddAppraisal.aspx...")
            await page.goto('https://nadlanvaluation.spurams.com/AddAppraisal.aspx')
            await page.wait_for_load_state("networkidle")
            print(f"   Current URL: {page.url}")
            
            print("2. Filling login credentials...")
            await page.wait_for_selector('#ctl00_cphBody_Login1_UserName', timeout=5000)
            await page.fill('#ctl00_cphBody_Login1_UserName', variables['username'])
            await page.fill('#ctl00_cphBody_Login1_Password', variables['password'])
            
            print("3. Clicking login button...")
            await page.click('#ctl00_cphBody_Login1_LoginButton')
            await page.wait_for_load_state("networkidle")
            print(f"   Current URL after login: {page.url}")
            
            # Wait a bit more to see if there's a redirect
            await page.wait_for_timeout(3000)
            print(f"   Final URL: {page.url}")
            
            # Check if we're on the AddAppraisal page
            if 'AddAppraisal.aspx' in page.url:
                print("✅ SUCCESS: Redirected to AddAppraisal.aspx!")
            else:
                print("❌ FAILED: Not redirected to AddAppraisal.aspx")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_url_after_login())
