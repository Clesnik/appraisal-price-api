import asyncio
import json
from playwright.async_api import async_playwright

async def debug_form_fields():
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
            
            print("4. Testing form fields one by one...")
            
            # Test each field selector
            fields_to_test = [
                ('#ctl00_cphBody_drpTransactionType', 'Transaction Type'),
                ('#ctl00_cphBody_drpLoanType', 'Loan Type'),
                ('#ctl00_cphBody_txtLoanNumber', 'Loan Number'),
                ('#ctl00_cphBody_txtBorrowerName', 'Borrower Name'),
                ('#ctl00_cphBody_drpPropertyType', 'Property Type'),
                ('#ctl00_cphBody_txtPropertyAddress', 'Property Address'),
                ('#ctl00_cphBody_txtPropertyCity', 'Property City'),
                ('#ctl00_cphBody_drpPropertyState', 'Property State'),
                ('#ctl00_cphBody_txtPropertyZip', 'Property Zip'),
                ('#ctl00_cphBody_drpOccupancyType', 'Occupancy Type'),
                ('#ctl00_cphBody_drpContactPerson', 'Contact Person'),
                ('#ctl00_cphBody_txtAccessInstructions', 'Access Instructions'),
                ('#ctl00_cphBody_txtAgentName', 'Agent Name'),
                ('#ctl00_cphBody_drpProject', 'Project/Appraisal Type'),
                ('#ctl00_cphBody_txtDateNeeded', 'Date Needed'),
                ('#ctl00_cphBody_lblAppraisalFee', 'Appraisal Fee')
            ]
            
            for selector, field_name in fields_to_test:
                try:
                    print(f"Testing {field_name} ({selector})...")
                    element = await page.wait_for_selector(selector, timeout=3000)
                    if element:
                        print(f"✅ {field_name} found successfully")
                    else:
                        print(f"❌ {field_name} not found")
                except Exception as e:
                    print(f"❌ {field_name} failed: {e}")
                
                await page.wait_for_timeout(500)
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_form_fields())
