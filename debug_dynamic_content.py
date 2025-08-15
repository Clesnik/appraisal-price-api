import asyncio
from playwright.async_api import async_playwright

async def debug_dynamic_content():
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
            
            # Click Continue button
            print("⏳ Clicking Continue button...")
            await page.click('#ctl00_cphBody_btnContinue')
            print("✅ Continue button clicked")
            
            # Wait for any dynamic content to load
            print("⏳ Waiting for dynamic content to load...")
            
            # Monitor for changes over time
            for i in range(10):  # Check for 10 seconds
                print(f"\n--- Check {i+1}/10 ---")
                
                # Wait a bit
                await page.wait_for_timeout(1000)
                
                # Check current URL
                current_url = page.url
                print(f"Current URL: {current_url}")
                
                # Look for any elements with fee-related content
                try:
                    # Check for the original fee element
                    fee_element = await page.query_selector('#ctl00_cphBody_lblAppraisalFee')
                    if fee_element:
                        is_visible = await fee_element.is_visible()
                        text_content = await fee_element.text_content()
                        print(f"  ✅ Found appraisal fee: {text_content} (Visible: {is_visible})")
                        break
                    else:
                        print("  ❌ Appraisal fee element not found")
                except Exception as e:
                    print(f"  ⚠️ Error checking fee element: {e}")
                
                # Look for any elements containing dollar signs or numbers that might be fees
                try:
                    all_elements = await page.query_selector_all('*')
                    fee_candidates = []
                    
                    for element in all_elements[:100]:  # Check first 100 elements
                        try:
                            text = await element.text_content()
                            if text and ('$' in text or any(word in text.lower() for word in ['fee', 'price', 'cost', 'amount'])):
                                element_id = await element.get_attribute('id')
                                element_class = await element.get_attribute('class')
                                is_visible = await element.is_visible()
                                
                                if is_visible and text.strip():
                                    fee_candidates.append({
                                        'text': text.strip(),
                                        'id': element_id,
                                        'class': element_class
                                    })
                        except:
                            pass
                    
                    if fee_candidates:
                        print(f"  🔍 Found {len(fee_candidates)} potential fee elements:")
                        for candidate in fee_candidates[:5]:  # Show first 5
                            print(f"    - '{candidate['text']}' (ID: {candidate['id']}, Class: {candidate['class']})")
                    else:
                        print("  🔍 No potential fee elements found")
                        
                except Exception as e:
                    print(f"  ⚠️ Error searching for fee candidates: {e}")
                
                # Check if page title changed
                try:
                    page_title = await page.title()
                    print(f"  📄 Page title: {page_title}")
                except:
                    pass
            
            # Take final screenshot
            await page.screenshot(path="final_debug.png")
            print("📸 Final screenshot saved as final_debug.png")
            
            # Keep browser open for manual inspection
            print("\n🔍 Browser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_dynamic_content())
