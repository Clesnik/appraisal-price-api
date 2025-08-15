import asyncio
from playwright.async_api import async_playwright

async def test_zip_occupancy():
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
            await page.wait_for_load_state("domcontentloaded")
            
            print("2. Filling login credentials...")
            await page.wait_for_selector('#ctl00_cphBody_Login1_UserName', timeout=5000)
            await page.fill('#ctl00_cphBody_Login1_UserName', variables['username'])
            await page.fill('#ctl00_cphBody_Login1_Password', variables['password'])
            
            print("3. Clicking login button...")
            await page.click('#ctl00_cphBody_Login1_LoginButton')
            await page.wait_for_load_state("domcontentloaded")
            await page.wait_for_timeout(2000)
            
            print("4. Filling basic fields...")
            # Fill some basic fields first
            await page.select_option('#ctl00_cphBody_drpTransactionType', '1')
            await page.select_option('#ctl00_cphBody_drpLoanType', '5')
            await page.fill('#ctl00_cphBody_txtPropertyAddress', '15 Burr Avenue')
            await page.fill('#ctl00_cphBody_txtPropertyCity', 'Marlboro Township')
            await page.select_option('#ctl00_cphBody_drpPropertyState', 'NJ')
            
            print("5. FILLING ZIP CODE...")
            await page.fill('#ctl00_cphBody_txtPropertyZip', '07751')
            print("✅ ZIP CODE FILLED")
            
            print("6. WAITING 3 SECONDS...")
            await page.wait_for_timeout(3000)
            
            print("7. SELECTING OCCUPANCY TYPE...")
            await page.select_option('#ctl00_cphBody_drpOccupiedBy', 'Investment')
            print("✅ OCCUPANCY TYPE SELECTED")
            
            print("8. Waiting 5 seconds to verify...")
            await page.wait_for_timeout(5000)
            
            # Check final values
            zip_value = await page.eval_on_selector('#ctl00_cphBody_txtPropertyZip', 'el => el.value')
            occupancy_value = await page.eval_on_selector('#ctl00_cphBody_drpOccupiedBy', 'el => el.value')
            
            print(f"Final ZIP value: '{zip_value}'")
            print(f"Final OCCUPANCY value: '{occupancy_value}'")
            
            if zip_value == '07751' and occupancy_value == 'Investment':
                print("🎉 SUCCESS: BOTH ZIP AND OCCUPANCY WORKED!")
            else:
                print("❌ FAILED: One or both didn't work")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_zip_occupancy())
