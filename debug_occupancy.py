import asyncio
from playwright.async_api import async_playwright

async def debug_occupancy():
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
            await page.fill('#ctl00_cphBody_txtPropertyZip', '07751')
            
            print("5. WAITING 2 SECONDS before occupancy type...")
            await page.wait_for_timeout(2000)
            
            print("6. Testing occupancy type dropdown...")
            
            # Check if the element exists
            try:
                element = await page.wait_for_selector('#ctl00_cphBody_drpOccupiedBy', timeout=5000)
                print("✅ Occupancy dropdown found!")
                
                # Check current value
                current_value = await page.eval_on_selector('#ctl00_cphBody_drpOccupiedBy', 'el => el.value')
                print(f"Current value: '{current_value}'")
                
                # Try to select Investment
                print("Trying to select 'Investment'...")
                await page.select_option('#ctl00_cphBody_drpOccupiedBy', 'Investment')
                await page.wait_for_timeout(1000)
                
                # Check if it worked
                new_value = await page.eval_on_selector('#ctl00_cphBody_drpOccupiedBy', 'el => el.value')
                print(f"New value: '{new_value}'")
                
                if new_value == 'Investment':
                    print("✅ SUCCESS: Occupancy type selected!")
                else:
                    print("❌ FAILED: Value didn't change")
                    
            except Exception as e:
                print(f"❌ Error with occupancy dropdown: {e}")
                
            print("7. Waiting 10 seconds to see result...")
            await page.wait_for_timeout(10000)
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_occupancy())
