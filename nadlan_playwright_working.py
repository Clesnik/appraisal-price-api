import asyncio
import json
import sys
from playwright.async_api import async_playwright
from datetime import datetime

class NadlanPlaywrightWorking:
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

    async def safe_fill_field(self, page, selector, value, field_name, timeout=3000):
        """Safely fill a field if it exists and value is valid"""
        if not self.is_valid_value(value):
            print(f"⏭️ Skipping {field_name} (empty or invalid)")
            return True
            
        try:
            await page.wait_for_selector(selector, timeout=timeout)
            await page.fill(selector, value)
            print(f"✅ Filled {field_name} with: {value}")
            await page.wait_for_timeout(200)
            return True
        except Exception as e:
            print(f"❌ Failed to fill {field_name}: {e}")
            return False

    async def safe_select_option(self, page, selector, value, field_name, value_map=None, timeout=3000):
        """Safely select an option if the field exists and value is valid"""
        if not self.is_valid_value(value):
            print(f"⏭️ Skipping {field_name} (empty or invalid)")
            return True
            
        try:
            await page.wait_for_selector(selector, timeout=timeout)
            if value_map:
                actual_value = value_map.get(value, value)
            else:
                actual_value = value
            await page.select_option(selector, actual_value)
            print(f"✅ Selected {field_name}: {value} (value: {actual_value})")
            await page.wait_for_timeout(200)
            return True
        except Exception as e:
            print(f"❌ Failed to select {field_name}: {e}")
            return False

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
                                transaction_type_map = {
                                    'Acquisition': '27', 'Construction': '23', 'FHA': '21', 'HELOC': '34',
                                    'Home Equity Line of Credit': '18', 'Investment Property': '9',
                                    'List Price Determination': '17', 'Market Value': '15',
                                    'Market Value for Lender Purposes': '19', 'Other': '14',
                                    'Purchase': '1', 'Refinance': '2', 'Reverse Mortgage': '16',
                                    'Second Mortgage': '24'
                                }
                                await self.safe_select_option(
                                    page, '#ctl00_cphBody_drpTransactionType',
                                    self.variables.get('transaction_type'), 'Transaction Type',
                                    transaction_type_map
                                )
                                
                                # Loan Type
                                loan_type_map = {
                                    'Conventional': '1', 'ConvInsured': '15', 'FHA': '3', 'FHA 203K': '12',
                                    'HARP 2': '7', 'Home Equity': '8', 'Home Ownership Accelerator': '9',
                                    'Homestyle Renovation': '13', 'Jumbo': '10', 'List Price Determination': '6',
                                    'Non QM': '16', 'Non-Conforming': '18', 'Other (please specify)': '5',
                                    'Prime Jumbo': '17', 'Public And Indian Housing': '14',
                                    'Reverse Mortgage': '11', 'USDA / Rural Housing Service': '4', 'VA': '2'
                                }
                                await self.safe_select_option(
                                    page, '#ctl00_cphBody_drpLoanType',
                                    self.variables.get('loan_type'), 'Loan Type',
                                    loan_type_map
                                )
                                
                                # Loan Number
                                await self.safe_fill_field(
                                    page, '#ctl00_cphBody_txtLoanNumber',
                                    self.variables.get('loan_number'), 'Loan Number'
                                )
                                
                                # Borrower Name
                                await self.safe_fill_field(
                                    page, '#ctl00_cphBody_txtBorrowerName',
                                    self.variables.get('borrower'), 'Borrower Name'
                                )
                                
                                # Property Type
                                property_type_map = {
                                    'Condo': '1', 'Co-op': '2', 'Duplex': '3', 'Fourplex': '4',
                                    'High Rise': '5', 'Land': '6', 'Manufactured Home': '7',
                                    'Mixed Use': '8', 'Mobile Home': '9', 'Multi-Family': '10',
                                    'Office': '11', 'Retail': '12', 'Single Family Residential': '13',
                                    'Townhouse': '14', 'Triplex': '15'
                                }
                                await self.safe_select_option(
                                    page, '#ctl00_cphBody_drpPropertyType',
                                    self.variables.get('property_type'), 'Property Type',
                                    property_type_map
                                )
                                
                                # Property Address
                                await self.safe_fill_field(
                                    page, '#ctl00_cphBody_txtPropertyAddress',
                                    self.variables.get('property_address'), 'Property Address'
                                )
                                
                                # Property City
                                await self.safe_fill_field(
                                    page, '#ctl00_cphBody_txtPropertyCity',
                                    self.variables.get('property_city'), 'Property City'
                                )
                                
                                # Property State
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
                                await self.safe_select_option(
                                    page, '#ctl00_cphBody_drpPropertyState',
                                    self.variables.get('property_state'), 'Property State',
                                    state_map
                                )
                                
                                # Property Zip (ROBUST METHOD)
                                property_zip = self.variables.get('property_zip')
                                if self.is_valid_value(property_zip):
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtPropertyZip', timeout=3000)
                                        # Click, clear, type character by character
                                        await page.click('#ctl00_cphBody_txtPropertyZip')
                                        await page.wait_for_timeout(500)
                                        await page.fill('#ctl00_cphBody_txtPropertyZip', '')
                                        await page.wait_for_timeout(500)
                                        
                                        # Type character by character
                                        for char in property_zip:
                                            await page.type('#ctl00_cphBody_txtPropertyZip', char)
                                            await page.wait_for_timeout(100)
                                        
                                        print(f"✅ Filled Property Zip with: {property_zip}")
                                        await page.wait_for_timeout(500)
                                    except Exception as e:
                                        print(f"❌ Failed to fill Property Zip: {e}")
                                else:
                                    print("⏭️ Skipping Property Zip (empty or invalid)")
                                
                                # Add delay after zip code to ensure page is ready
                                print("⏳ Waiting 3 seconds after zip code...")
                                await page.wait_for_timeout(3000)
                                
                                # Occupancy Type (ROBUST METHOD)
                                occupancy_type = self.variables.get('occupancy_type')
                                if self.is_valid_value(occupancy_type):
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_drpOccupiedBy', timeout=5000)
                                        # Click dropdown first, then select
                                        await page.click('#ctl00_cphBody_drpOccupiedBy')
                                        await page.wait_for_timeout(500)
                                        
                                        occupancy_map = {
                                            'Owner Occupied': 'Owner',
                                            'Investment': 'Investment',
                                            'Second Home': 'Secondaryresidence',
                                            'Primary Residence': 'Primaryresidence',
                                            'Tenant': 'Tenant',
                                            'Vacant': 'Vacant'
                                        }
                                        occupancy_value = occupancy_map.get(occupancy_type, occupancy_type)
                                        await page.select_option('#ctl00_cphBody_drpOccupiedBy', occupancy_value)
                                        print(f"✅ Selected occupancy type: {occupancy_type} (value: {occupancy_value})")
                                        await page.wait_for_timeout(500)
                                    except Exception as e:
                                        print(f"❌ Failed to select occupancy type: {e}")
                                else:
                                    print("⏭️ Skipping occupancy type (empty or invalid)")
                                
                                # Agent Name (ROBUST METHOD)
                                agent_name = self.variables.get('agent_name')
                                if self.is_valid_value(agent_name):
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtAgentName', timeout=3000)
                                        await page.click('#ctl00_cphBody_txtAgentName')
                                        await page.wait_for_timeout(200)
                                        await page.fill('#ctl00_cphBody_txtAgentName', '')
                                        await page.wait_for_timeout(200)
                                        await page.fill('#ctl00_cphBody_txtAgentName', agent_name)
                                        print(f"✅ Filled Agent Name with: {agent_name}")
                                        await page.wait_for_timeout(500)
                                    except Exception as e:
                                        print(f"❌ Failed to fill Agent Name: {e}")
                                else:
                                    print("⏭️ Skipping Agent Name (empty or invalid)")
                                
                                # Contact Person (ROBUST METHOD)
                                contact_person = self.variables.get('contact_person')
                                if self.is_valid_value(contact_person):
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_drpAppointmentContact', timeout=3000)
                                        await page.click('#ctl00_cphBody_drpAppointmentContact')
                                        await page.wait_for_timeout(500)
                                        contact_map = {
                                            'Borrower': 'borrower',
                                            'Agent': 'agent',
                                            'Other': 'other'
                                        }
                                        contact_value = contact_map.get(contact_person, contact_person.lower())
                                        await page.select_option('#ctl00_cphBody_drpAppointmentContact', contact_value)
                                        print(f"✅ Selected contact person: {contact_person} (value: {contact_value})")
                                        await page.wait_for_timeout(500)
                                    except Exception as e:
                                        print(f"❌ Failed to select contact person: {e}")
                                else:
                                    print("⏭️ Skipping contact person (empty or invalid)")
                                
                                # Access Instructions (ROBUST METHOD)
                                access_instructions = self.variables.get('other_access_instructions')
                                if self.is_valid_value(access_instructions):
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtAccessInformation', timeout=3000)
                                        await page.click('#ctl00_cphBody_txtAccessInformation')
                                        await page.wait_for_timeout(200)
                                        await page.fill('#ctl00_cphBody_txtAccessInformation', '')
                                        await page.wait_for_timeout(200)
                                        await page.fill('#ctl00_cphBody_txtAccessInformation', access_instructions)
                                        print(f"✅ Filled Access Instructions with: {access_instructions}")
                                        await page.wait_for_timeout(500)
                                    except Exception as e:
                                        print(f"❌ Failed to fill Access Instructions: {e}")
                                else:
                                    print("⏭️ Skipping Access Instructions (empty or invalid)")
                                
                                # Date Needed (ROBUST METHOD)
                                date_needed = self.variables.get('date_appraisal_needed')
                                if self.is_valid_value(date_needed):
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtDateNeeded', timeout=3000)
                                        await page.click('#ctl00_cphBody_txtDateNeeded')
                                        await page.wait_for_timeout(200)
                                        await page.fill('#ctl00_cphBody_txtDateNeeded', '')
                                        await page.wait_for_timeout(200)
                                        await page.fill('#ctl00_cphBody_txtDateNeeded', date_needed)
                                        print(f"✅ Filled Date Needed with: {date_needed}")
                                        await page.wait_for_timeout(500)
                                    except Exception as e:
                                        print(f"❌ Failed to fill Date Needed: {e}")
                                else:
                                    print("⏭️ Skipping Date Needed (empty or invalid)")
                                
                                # Product/Appraisal Type (ROBUST METHOD)
                                product = self.variables.get('product')
                                if self.is_valid_value(product):
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_drpAppraisalType', timeout=3000)
                                        await page.click('#ctl00_cphBody_drpAppraisalType')
                                        await page.wait_for_timeout(500)
                                        product_str = str(product)
                                        await page.select_option('#ctl00_cphBody_drpAppraisalType', product_str)
                                        print(f"✅ Selected product/appraisal type: {product} (value: {product_str})")
                                        await page.wait_for_timeout(500)
                                    except Exception as e:
                                        print(f"❌ Failed to select product/appraisal type: {e}")
                                else:
                                    print("⏭️ Skipping product/appraisal type (empty or invalid)")
                                
                                print("✅ All available fields filled successfully!")
                                
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
                                                        "property_state", "property_zip", "agent_name", "date_needed"]
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
        print("Usage: python nadlan_playwright_working.py '<json_variables>'")
        sys.exit(1)
    
    try:
        variables_json = sys.argv[1]
        print(f"DEBUG: Raw input: {variables_json}")
        
        variables = json.loads(variables_json)
        print(f"DEBUG: Parsed variables: {variables}")
        
        nadlan = NadlanPlaywrightWorking(variables)
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
