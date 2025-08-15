import asyncio
from playwright.async_api import async_playwright

async def debug_fee_content():
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
            
            # Wait 1 second as requested
            await page.wait_for_timeout(1000)
            
            # Get page content
            page_content = await page.content()
            
            # Find the position of "Appraisal Fee" in the content
            fee_index = page_content.find('Appraisal Fee')
            if fee_index != -1:
                print(f"✅ Found 'Appraisal Fee' at position {fee_index}")
                
                # Show the content around "Appraisal Fee"
                start = max(0, fee_index - 100)
                end = min(len(page_content), fee_index + 200)
                context = page_content[start:end]
                
                print("\n🔍 Content around 'Appraisal Fee':")
                print("=" * 50)
                print(context)
                print("=" * 50)
                
                # Try different regex patterns
                import re
                patterns = [
                    r'Appraisal Fee[:\s]*\$([\d,]+\.?\d*)',
                    r'Appraisal Fee.*?(\$[\d,]+\.?\d*)',
                    r'Appraisal Fee[^$]*(\$[\d,]+\.?\d*)',
                    r'Appraisal Fee[^<]*?(\$[\d,]+\.?\d*)',
                ]
                
                for i, pattern in enumerate(patterns):
                    print(f"\n🔍 Trying pattern {i+1}: {pattern}")
                    match = re.search(pattern, context, re.DOTALL)
                    if match:
                        print(f"✅ Pattern {i+1} matched: {match.group(0)}")
                        print(f"   Dollar amount: {match.group(1)}")
                    else:
                        print(f"❌ Pattern {i+1} did not match")
                
            else:
                print("❌ 'Appraisal Fee' not found in page content")
            
            # Take a screenshot
            await page.screenshot(path="debug_fee_content.png")
            print("📸 Screenshot saved as debug_fee_content.png")
            
            # Keep browser open for manual inspection
            print("\n🔍 Browser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_fee_content())
