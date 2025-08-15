import asyncio
from playwright.async_api import async_playwright

async def debug_fee_without_continue():
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
            
            # Wait a bit for any calculations to happen
            print("⏳ Waiting for potential fee calculation...")
            await page.wait_for_timeout(3000)
            
            # Take a screenshot
            await page.screenshot(path="fee_search.png")
            print("📸 Screenshot saved as fee_search.png")
            
            # Look for the appraisal fee element specifically
            print("\n🔍 Looking for appraisal fee element...")
            try:
                fee_element = await page.query_selector('#ctl00_cphBody_lblAppraisalFee')
                if fee_element:
                    is_visible = await fee_element.is_visible()
                    text_content = await fee_element.text_content()
                    print(f"  ✅ Found appraisal fee element:")
                    print(f"    Visible: {is_visible}")
                    print(f"    Text: '{text_content}'")
                    print(f"    Display style: {await fee_element.evaluate('el => getComputedStyle(el).display')}")
                    print(f"    Visibility: {await fee_element.evaluate('el => getComputedStyle(el).visibility')}")
                else:
                    print("  ❌ Appraisal fee element not found")
            except Exception as e:
                print(f"  ⚠️ Error checking fee element: {e}")
            
            # Look for any elements containing dollar signs
            print("\n🔍 Looking for any elements with dollar signs...")
            try:
                all_elements = await page.query_selector_all('*')
                dollar_elements = []
                
                for element in all_elements:
                    try:
                        text = await element.text_content()
                        if text and '$' in text:
                            element_id = await element.get_attribute('id')
                            element_class = await element.get_attribute('class')
                            is_visible = await element.is_visible()
                            
                            if is_visible:
                                dollar_elements.append({
                                    'text': text.strip(),
                                    'id': element_id,
                                    'class': element_class
                                })
                    except:
                        pass
                
                if dollar_elements:
                    print(f"  Found {len(dollar_elements)} elements with dollar signs:")
                    for elem in dollar_elements:
                        print(f"    - '{elem['text']}' (ID: {elem['id']}, Class: {elem['class']})")
                else:
                    print("  No elements with dollar signs found")
                    
            except Exception as e:
                print(f"  ⚠️ Error searching for dollar elements: {e}")
            
            # Look for any labels or spans that might contain fee information
            print("\n🔍 Looking for fee-related labels and spans...")
            try:
                labels = await page.query_selector_all('label, span, div')
                fee_labels = []
                
                for label in labels:
                    try:
                        label_text = await label.text_content()
                        if label_text and any(term in label_text.lower() for term in ['fee', 'price', 'cost', 'amount', 'appraisal']):
                            label_id = await label.get_attribute('id')
                            label_class = await label.get_attribute('class')
                            is_visible = await label.is_visible()
                            
                            if is_visible and label_text.strip():
                                fee_labels.append({
                                    'text': label_text.strip(),
                                    'id': label_id,
                                    'class': label_class
                                })
                    except:
                        pass
                
                if fee_labels:
                    print(f"  Found {len(fee_labels)} fee-related labels:")
                    for label in fee_labels[:10]:  # Show first 10
                        print(f"    - '{label['text']}' (ID: {label['id']}, Class: {label['class']})")
                else:
                    print("  No fee-related labels found")
                    
            except Exception as e:
                print(f"  ⚠️ Error searching for fee labels: {e}")
            
            # Look for any hidden elements that might contain the fee
            print("\n🔍 Looking for hidden elements that might contain fee...")
            try:
                hidden_elements = await page.query_selector_all('[style*="display: none"], [style*="visibility: hidden"], [hidden]')
                print(f"  Found {len(hidden_elements)} hidden elements")
                
                for i, element in enumerate(hidden_elements[:5]):  # Check first 5
                    try:
                        element_id = await element.get_attribute('id')
                        element_text = await element.text_content()
                        if element_text and any(term in element_text.lower() for term in ['fee', 'price', 'cost', '$']):
                            print(f"    Hidden element {i+1}: '{element_text}' (ID: {element_id})")
                    except:
                        pass
                        
            except Exception as e:
                print(f"  ⚠️ Error searching for hidden elements: {e}")
            
            # Check if there are any JavaScript variables or data attributes that might contain the fee
            print("\n🔍 Checking for JavaScript variables or data attributes...")
            try:
                # Look for any data attributes that might contain fee information
                data_elements = await page.query_selector_all('[data-*]')
                print(f"  Found {len(data_elements)} elements with data attributes")
                
                for i, element in enumerate(data_elements[:10]):  # Check first 10
                    try:
                        element_id = await element.get_attribute('id')
                        data_attrs = await element.evaluate('el => Object.keys(el.dataset)')
                        if data_attrs:
                            print(f"    Element {i+1} (ID: {element_id}) has data attributes: {data_attrs}")
                    except:
                        pass
                        
            except Exception as e:
                print(f"  ⚠️ Error checking data attributes: {e}")
            
            # Keep browser open for manual inspection
            print("\n🔍 Browser will stay open for 30 seconds for manual inspection...")
            await page.wait_for_timeout(30000)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_fee_without_continue())
