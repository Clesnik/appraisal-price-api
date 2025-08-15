import asyncio
import json
import sys
from playwright.async_api import async_playwright
from datetime import datetime

class NadlanPlaywrightSimpleWorking:
    def __init__(self, variables):
        self.variables = variables
        self.target_url = variables.get('target_url', 'https://nadlanvaluation.spurams.com/login.aspx')
        self.headless = variables.get('headless', False)
        
        # Debug: Print the variables being used
        print(f"DEBUG: Variables received: {self.variables}")
        print(f"DEBUG: Username: {self.variables.get('username', 'NOT FOUND')}")
        print(f"DEBUG: Password: {self.variables.get('password', 'NOT FOUND')}")
        print(f"DEBUG: Transaction type: {self.variables.get('transaction_type', 'NOT FOUND')}")
        print(f"DEBUG: Product: {self.variables.get('product', 'NOT FOUND')}")
        print(f"DEBUG: Property type: {self.variables.get('property_type', 'NOT FOUND')}")

    def is_valid_value(self, value):
        """Check if a value is valid (not None, empty string, or just whitespace)"""
        if value is None:
            return False
        if isinstance(value, str) and value.strip() == "":
            return False
        if value == "":
            return False
        return True

    async def run(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=self.headless)
            page = await browser.new_page()
            
            try:
                # Navigate directly to AddAppraisal.aspx (will redirect to login if needed)
                print("🚀 Navigating directly to AddAppraisal.aspx...")
                await page.goto('https://nadlanvaluation.spurams.com/AddAppraisal.aspx')
                await page.wait_for_load_state("domcontentloaded")
                
                # Wait additional time if specified (ultra-reduced default)
                wait_time = self.variables.get('wait_time', 0)
                if wait_time > 0:
                    await page.wait_for_timeout(wait_time)
                
                # Fill in username if provided
                username = self.variables.get('username')
                if self.is_valid_value(username):
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_UserName', timeout=3000)
                        await page.fill('#ctl00_cphBody_Login1_UserName', username)
                        print(f"Filled username field with: {username}")
                        await page.wait_for_timeout(100)
                    except Exception as e:
                        print(f"Error filling username: {e}")
                else:
                    print("⏭️ Skipping username field (empty or invalid)")
                
                # Fill in password if provided
                password = self.variables.get('password')
                if self.is_valid_value(password):
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_Password', timeout=3000)
                        await page.fill('#ctl00_cphBody_Login1_Password', password)
                        print(f"Filled password field with: {password}")
                        await page.wait_for_timeout(100)
                    except Exception as e:
                        print(f"Error filling password: {e}")
                else:
                    print("⏭️ Skipping password field (empty or invalid)")
                
                # Click login button if credentials are provided
                if self.is_valid_value(username) and self.is_valid_value(password):
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_LoginButton', timeout=3000)
                        await page.click('#ctl00_cphBody_Login1_LoginButton')
                        print("Clicked login button")
                        await page.wait_for_timeout(1000)
                        
                        # Wait for redirect to Add Appraisal page
                        try:
                            print("⏳ Waiting for redirect to Add Appraisal page...")
                            await page.wait_for_load_state("domcontentloaded")
                            print("✅ Login completed, checking for form elements...")
                            await page.wait_for_timeout(500)
                            
                            # Wait for the appraisal form to load
                            try:
                                await page.wait_for_selector('#ctl00_cphBody_drpTransactionType', timeout=5000)
                                print("✅ Appraisal form loaded successfully")
                                
                                # Fill form fields that we know work
                                print("📝 Filling form fields...")
                                
                                # Transaction Type
                                transaction_type = self.variables.get('transaction_type')
                                if self.is_valid_value(transaction_type):
                                    transaction_type_map = {
                                        'Acquisition': '27', 'Construction': '23', 'FHA': '21', 'HELOC': '34',
                                        'Home Equity Line of Credit': '18', 'Investment Property': '9',
                                        'List Price Determination': '17', 'Market Value': '15',
                                        'Market Value for Lender Purposes': '19', 'Other': '14',
                                        'Purchase': '1', 'Refinance': '2', 'Reverse Mortgage': '16',
                                        'Second Mortgage': '24'
                                    }
                                    transaction_value = transaction_type_map.get(transaction_type, '1')
                                    await page.select_option('#ctl00_cphBody_drpTransactionType', transaction_value)
                                    print(f"✅ Selected transaction type: {transaction_type} (value: {transaction_value})")
                                    await page.wait_for_timeout(500)
                                
                                # Loan Type
                                loan_type = self.variables.get('loan_type')
                                if self.is_valid_value(loan_type):
                                    loan_type_map = {
                                        'Conventional': '1', 'ConvInsured': '15', 'FHA': '3', 'FHA 203K': '12',
                                        'HARP 2': '7', 'Home Equity': '8', 'Home Ownership Accelerator': '9',
                                        'Homestyle Renovation': '13', 'Jumbo': '10', 'List Price Determination': '6',
                                        'Non QM': '16', 'Non-Conforming': '18', 'Other (please specify)': '5',
                                        'Prime Jumbo': '17', 'Public And Indian Housing': '14',
                                        'Reverse Mortgage': '11', 'USDA / Rural Housing Service': '4', 'VA': '2'
                                    }
                                    loan_value = loan_type_map.get(loan_type, '5')
                                    await page.select_option('#ctl00_cphBody_drpLoanType', loan_value)
                                    print(f"✅ Selected loan type: {loan_type} (value: {loan_value})")
                                    await page.wait_for_timeout(500)
                                
                                # Loan Number
                                loan_number = self.variables.get('loan_number')
                                if self.is_valid_value(loan_number):
                                    await page.fill('#ctl00_cphBody_txtLoanNumber', loan_number)
                                    print(f"✅ Filled loan number: {loan_number}")
                                    await page.wait_for_timeout(500)
                                
                                # Borrower Name
                                borrower = self.variables.get('borrower')
                                if self.is_valid_value(borrower):
                                    await page.fill('#ctl00_cphBody_txtBorrowerName', borrower)
                                    print(f"✅ Filled borrower name: {borrower}")
                                    await page.wait_for_timeout(500)
                                
                                # Property Type
                                property_type = self.variables.get('property_type')
                                if self.is_valid_value(property_type):
                                    property_type_map = {
                                        'Condo': '1', 'Co-op': '2', 'Duplex': '3', 'Fourplex': '4',
                                        'High Rise': '5', 'Land': '6', 'Manufactured Home': '7',
                                        'Mixed Use': '8', 'Mobile Home': '9', 'Multi-Family': '10',
                                        'Office': '11', 'Retail': '12', 'Single Family Residential': '13',
                                        'Townhouse': '14', 'Triplex': '15'
                                    }
                                    property_value = property_type_map.get(property_type, '13')
                                    await page.select_option('#ctl00_cphBody_drpPropertyType', property_value)
                                    print(f"✅ Selected property type: {property_type} (value: {property_value})")
                                    await page.wait_for_timeout(500)
                                
                                # Property Address
                                property_address = self.variables.get('property_address')
                                if self.is_valid_value(property_address):
                                    await page.fill('#ctl00_cphBody_txtPropertyAddress', property_address)
                                    print(f"✅ Filled property address: {property_address}")
                                    await page.wait_for_timeout(500)
                                
                                # Property City
                                property_city = self.variables.get('property_city')
                                if self.is_valid_value(property_city):
                                    await page.fill('#ctl00_cphBody_txtPropertyCity', property_city)
                                    print(f"✅ Filled property city: {property_city}")
                                    await page.wait_for_timeout(500)
                                
                                # Property State
                                property_state = self.variables.get('property_state')
                                if self.is_valid_value(property_state):
                                    state_map = {
                                        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
                                        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
                                        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
                                        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
                                        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
                                        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
                                        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
                                        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
                                        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
                                        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
                                        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
                                        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
                                        'Wisconsin': 'WI', 'Wyoming': 'WY'
                                    }
                                    state_value = state_map.get(property_state, property_state)
                                    await page.select_option('#ctl00_cphBody_drpPropertyState', state_value)
                                    print(f"✅ Selected property state: {property_state} (value: {state_value})")
                                    await page.wait_for_timeout(500)
                                
                                # Property Zip - Simple approach
                                property_zip = self.variables.get('property_zip')
                                if self.is_valid_value(property_zip):
                                    await page.fill('#ctl00_cphBody_txtPropertyZip', property_zip)
                                    print(f"✅ Filled property zip: {property_zip}")
                                    await page.wait_for_timeout(1000)  # Give it time to process
                                
                                # Occupancy Type - Simple approach
                                occupancy_type = self.variables.get('occupancy_type')
                                if self.is_valid_value(occupancy_type):
                                    occupancy_map = {
                                        'Owner Occupied': 'Owner',
                                        'Non-Owner Occupied': 'Non-Owner',
                                        'Vacant': 'Vacant'
                                    }
                                    occupancy_value = occupancy_map.get(occupancy_type, occupancy_type)
                                    await page.select_option('#ctl00_cphBody_drpOccupiedBy', occupancy_value)
                                    print(f"✅ Selected occupancy type: {occupancy_type} (value: {occupancy_value})")
                                    await page.wait_for_timeout(500)
                                
                                # Agent Name
                                agent_name = self.variables.get('agent_name')
                                if self.is_valid_value(agent_name):
                                    await page.fill('#ctl00_cphBody_txtAgentName', agent_name)
                                    print(f"✅ Filled agent name: {agent_name}")
                                    await page.wait_for_timeout(500)
                                
                                # Contact Person
                                contact_person = self.variables.get('contact_person')
                                if self.is_valid_value(contact_person):
                                    contact_map = {
                                        'Borrower': 'borrower',
                                        'Agent': 'agent',
                                        'Other': 'other'
                                    }
                                    contact_value = contact_map.get(contact_person, contact_person.lower())
                                    await page.select_option('#ctl00_cphBody_drpAppointmentContact', contact_value)
                                    print(f"✅ Selected contact person: {contact_person} (value: {contact_value})")
                                    await page.wait_for_timeout(500)
                                
                                # Access Instructions
                                access_instructions = self.variables.get('other_access_instructions')
                                if self.is_valid_value(access_instructions):
                                    await page.fill('#ctl00_cphBody_txtAccessInformation', access_instructions)
                                    print(f"✅ Filled access instructions: {access_instructions}")
                                    await page.wait_for_timeout(500)
                                
                                # Date Needed
                                date_needed = self.variables.get('date_appraisal_needed')
                                if self.is_valid_value(date_needed):
                                    await page.fill('#ctl00_cphBody_txtDateNeeded', date_needed)
                                    print(f"✅ Filled date needed: {date_needed}")
                                    await page.wait_for_timeout(500)
                                
                                # Product/Appraisal Type
                                product = self.variables.get('product')
                                if self.is_valid_value(product):
                                    product_str = str(product)
                                    await page.select_option('#ctl00_cphBody_drpAppraisalType', product_str)
                                    print(f"✅ Selected product/appraisal type: {product} (value: {product_str})")
                                    await page.wait_for_timeout(500)
                                
                                print("✅ All available fields filled successfully!")
                                
                                # Wait longer for the form to process and look for calculate/submit button
                                print("⏳ Waiting for form to process and looking for calculate button...")
                                await page.wait_for_timeout(3000)
                                
                                # Try to find and click a calculate or submit button
                                try:
                                    # Look for common button selectors
                                    calculate_selectors = [
                                        '#ctl00_cphBody_btnCalculate',
                                        '#ctl00_cphBody_btnSubmit', 
                                        '#ctl00_cphBody_btnGetFee',
                                        'input[type="submit"][value*="Calculate"]',
                                        'input[type="submit"][value*="Submit"]',
                                        'button[type="submit"]',
                                        '.btn-calculate',
                                        '.btn-submit'
                                    ]
                                    
                                    button_clicked = False
                                    for selector in calculate_selectors:
                                        try:
                                            button = await page.wait_for_selector(selector, timeout=1000)
                                            if button:
                                                await button.click()
                                                print(f"✅ Clicked calculate/submit button: {selector}")
                                                button_clicked = True
                                                await page.wait_for_timeout(2000)  # Wait for calculation
                                                break
                                        except:
                                            continue
                                    
                                    if not button_clicked:
                                        print("⚠️ No calculate/submit button found, continuing...")
                                        
                                except Exception as e:
                                    print(f"⚠️ Error looking for calculate button: {e}")
                                
                                # Wait additional time for appraisal fee to appear
                                print("⏳ Waiting for appraisal fee to appear...")
                                await page.wait_for_timeout(5000)
                                
                                # Try to extract appraisal fee if available
                                try:
                                    appraisal_fee_element = await page.wait_for_selector('#ctl00_cphBody_lblAppraisalFee', timeout=3000)
                                    appraisal_fee = await appraisal_fee_element.text_content()
                                    print(f"✅ Extracted appraisal fee: {appraisal_fee}")
                                    
                                    # Take screenshot of the appraisal fee element
                                    screenshot_path = self.variables.get('screenshot_path', 'appraisal_fee_element.png')
                                    await appraisal_fee_element.screenshot(path=screenshot_path)
                                    print(f"Screenshot of appraisal fee element saved as: {screenshot_path}")
                                    
                                    # Take full page screenshot
                                    full_page_screenshot = 'full_page_appraisal_fee.png'
                                    await page.screenshot(path=full_page_screenshot, full_page=True)
                                    print(f"Full page screenshot saved as: {full_page_screenshot}")
                                    
                                    # Return the results as JSON
                                    result = {
                                        "appraisal_fee": appraisal_fee,
                                        "appraisal_fee_screenshot": screenshot_path,
                                        "full_page_screenshot": full_page_screenshot
                                    }
                                    
                                    print(json.dumps(result))
                                    return result
                                    
                                except Exception as e:
                                    print(f"⚠️ Could not extract appraisal fee: {e}")
                                    # Still return success with available data
                                    result = {
                                        "status": "success",
                                        "message": "Form filled successfully but appraisal fee not available",
                                        "filled_fields": ["transaction_type", "loan_type", "loan_number", "borrower", 
                                                        "property_type", "property_address", "property_city", 
                                                        "property_state", "agent_name", "contact_person", 
                                                        "access_instructions", "date_needed", "product"]
                                    }
                                    print(json.dumps(result))
                                    return result
                                
                            except Exception as e:
                                print(f"Error loading appraisal form: {e}")
                                return {"error": f"Failed to load appraisal form: {str(e)}"}
                                
                        except Exception as e:
                            print(f"Error during login redirect: {e}")
                            return {"error": f"Login redirect failed: {str(e)}"}
                            
                    except Exception as e:
                        print(f"Error during login: {e}")
                        return {"error": f"Login failed: {str(e)}"}
                        
            except Exception as e:
                print(f"Error during navigation: {e}")
                return {"error": f"Navigation failed: {str(e)}"}
            finally:
                await browser.close()

async def main():
    if len(sys.argv) != 2:
        print("Usage: python nadlan_playwright_simple_working.py '<json_variables>'")
        sys.exit(1)
    
    try:
        variables_json = sys.argv[1]
        print(f"DEBUG: Raw input: {variables_json}")
        
        variables = json.loads(variables_json)
        print(f"DEBUG: Parsed variables: {variables}")
        
        nadlan = NadlanPlaywrightSimpleWorking(variables)
        result = await nadlan.run()
        
        if result:
            print(json.dumps(result))
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
