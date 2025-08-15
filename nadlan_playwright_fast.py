import asyncio
import json
import sys
from playwright.async_api import async_playwright
from datetime import datetime

class NadlanPlaywrightFast:
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

    async def run(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=self.headless)
            page = await browser.new_page()
            
            try:
                # Navigate to Nadlan valuation login page
                await page.goto(self.target_url)
                await page.wait_for_load_state("networkidle")
                
                # Wait additional time if specified (reduced default)
                wait_time = self.variables.get('wait_time', 1000)  # Reduced from 5000 to 1000
                if wait_time > 0:
                    await page.wait_for_timeout(wait_time)
                
                # Fill in username if provided
                username = self.variables.get('username')
                if username:
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_UserName', timeout=5000)
                        await page.fill('#ctl00_cphBody_Login1_UserName', username)
                        print(f"Filled username field with: {username}")
                        await page.wait_for_timeout(200)  # Reduced from 1000 to 200
                    except Exception as e:
                        print(f"Error filling username: {e}")
                
                # Fill in password if provided
                password = self.variables.get('password')
                if password:
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_Password', timeout=5000)
                        await page.fill('#ctl00_cphBody_Login1_Password', password)
                        print(f"Filled password field with: {password}")
                        await page.wait_for_timeout(200)  # Reduced from 1000 to 200
                    except Exception as e:
                        print(f"Error filling password: {e}")
                
                # Click login button if credentials are provided
                if username and password:
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_LoginButton', timeout=5000)
                        await page.click('#ctl00_cphBody_Login1_LoginButton')
                        print("Clicked login button")
                        await page.wait_for_timeout(2000)  # Reduced from 5000 to 2000
                        
                        # Wait for dashboard to load
                        try:
                            await page.wait_for_selector('#ctl00_cphBody_btnAddAppraisal', timeout=10000)
                            print("Dashboard loaded successfully")
                            
                            # Click the "Create New Order" button
                            await page.click('#ctl00_cphBody_btnAddAppraisal')
                            print("Clicked 'Create New Order' button")
                            await page.wait_for_timeout(1000)  # Reduced from 3000 to 1000
                            
                            # Wait for the appraisal form to load
                            try:
                                await page.wait_for_selector('#ctl00_cphBody_drpTransactionType', timeout=10000)
                                print("Appraisal form loaded successfully")
                                
                                # Select transaction type if provided
                                transaction_type = self.variables.get('transaction_type')
                                if transaction_type:
                                    transaction_type_map = {
                                        'Acquisition': '27',
                                        'Construction': '23',
                                        'FHA': '21',
                                        'HELOC': '34',
                                        'Home Equity Line of Credit': '18',
                                        'Investment Property': '9',
                                        'List Price Determination': '17',
                                        'Market Value': '15',
                                        'Market Value for Lender Purposes': '19',
                                        'Other': '14',
                                        'Purchase': '1',
                                        'Refinance': '2',
                                        'Reverse Mortgage': '16',
                                        'Second Mortgage': '24'
                                    }
                                    transaction_value = transaction_type_map.get(transaction_type, '1')
                                    await page.select_option('#ctl00_cphBody_drpTransactionType', transaction_value)
                                    print(f"Selected transaction type: {transaction_type} (value: {transaction_value})")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Select loan type if provided
                                loan_type = self.variables.get('loan_type')
                                if loan_type:
                                    loan_type_map = {
                                        'Conventional': '1',
                                        'ConvInsured': '15',
                                        'FHA': '3',
                                        'FHA 203K': '12',
                                        'HARP 2': '7',
                                        'Home Equity': '8',
                                        'Home Ownership Accelerator': '9',
                                        'Homestyle Renovation': '13',
                                        'Jumbo': '10',
                                        'List Price Determination': '6',
                                        'Non QM': '16',
                                        'Non-Conforming': '18',
                                        'Other (please specify)': '5',
                                        'Prime Jumbo': '17',
                                        'Public And Indian Housing': '14',
                                        'Reverse Mortgage': '11',
                                        'USDA / Rural Housing Service': '4',
                                        'VA': '2'
                                    }
                                    loan_value = loan_type_map.get(loan_type, '5')
                                    await page.select_option('#ctl00_cphBody_drpLoanType', loan_value)
                                    print(f"Selected loan type: {loan_type} (value: {loan_value})")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Fill loan number if provided
                                loan_number = self.variables.get('loan_number')
                                if loan_number:
                                    await page.fill('#ctl00_cphBody_txtLoanNumber', loan_number)
                                    print(f"Filled loan number field with: {loan_number}")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Fill borrower name if provided
                                borrower = self.variables.get('borrower')
                                if borrower:
                                    await page.fill('#ctl00_cphBody_txtBorrowerName', borrower)
                                    print(f"Filled borrower name field with: {borrower}")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Select property type if provided
                                property_type = self.variables.get('property_type')
                                if property_type:
                                    property_type_map = {
                                        'Condo': '1',
                                        'Co-op': '2',
                                        'Duplex': '3',
                                        'Fourplex': '4',
                                        'High Rise': '5',
                                        'Land': '6',
                                        'Manufactured Home': '7',
                                        'Mixed Use': '8',
                                        'Mobile Home': '9',
                                        'Multi-Family': '10',
                                        'Office': '11',
                                        'Retail': '12',
                                        'Single Family Residential': '13',
                                        'Townhouse': '14',
                                        'Triplex': '15'
                                    }
                                    property_value = property_type_map.get(property_type, '13')
                                    await page.select_option('#ctl00_cphBody_drpPropertyType', property_value)
                                    print(f"Selected property type: {property_type} (value: {property_value})")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Fill property address if provided
                                property_address = self.variables.get('property_address')
                                if property_address:
                                    await page.fill('#ctl00_cphBody_txtPropertyAddress', property_address)
                                    print(f"Filled property address field with: {property_address}")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Fill property city if provided
                                property_city = self.variables.get('property_city')
                                if property_city:
                                    await page.fill('#ctl00_cphBody_txtPropertyCity', property_city)
                                    print(f"Filled property city field with: {property_city}")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Select property state if provided
                                property_state = self.variables.get('property_state')
                                if property_state:
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
                                    print(f"Selected property state: {property_state} (value: {state_value})")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Fill property zip if provided
                                property_zip = self.variables.get('property_zip')
                                if property_zip:
                                    await page.fill('#ctl00_cphBody_txtPropertyZip', property_zip)
                                    print(f"Filled property zip field with: {property_zip}")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Select occupancy type if provided
                                occupancy_type = self.variables.get('occupancy_type')
                                if occupancy_type:
                                    occupancy_map = {
                                        'Owner Occupied': 'Owner Occupied',
                                        'Investment': 'Investment',
                                        'Second Home': 'Second Home'
                                    }
                                    occupancy_value = occupancy_map.get(occupancy_type, occupancy_type)
                                    await page.select_option('#ctl00_cphBody_drpOccupancyType', occupancy_value)
                                    print(f"Selected occupancy type: {occupancy_type} (value: {occupancy_value})")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Select contact person if provided
                                contact_person = self.variables.get('contact_person')
                                if contact_person:
                                    contact_map = {
                                        'Borrower': 'borrower',
                                        'Agent': 'agent',
                                        'Lender': 'lender',
                                        'Other': 'other'
                                    }
                                    contact_value = contact_map.get(contact_person, contact_person.lower())
                                    await page.select_option('#ctl00_cphBody_drpContactPerson', contact_value)
                                    print(f"Selected contact person: {contact_person} (value: {contact_value})")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Fill access instructions if provided
                                access_instructions = self.variables.get('other_access_instructions')
                                if access_instructions:
                                    await page.fill('#ctl00_cphBody_txtAccessInstructions', access_instructions)
                                    print(f"Filled access instructions field with: {access_instructions}")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Fill agent name if provided
                                agent_name = self.variables.get('agent_name')
                                if agent_name:
                                    await page.fill('#ctl00_cphBody_txtAgentName', agent_name)
                                    print(f"Filled agent name field with: {agent_name}")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Select project/appraisal type if provided
                                product = self.variables.get('product')
                                if product:
                                    print(f"DEBUG: Product received: {product} (type: {type(product)})")
                                    product_str = str(product)
                                    print(f"DEBUG: Using product value: '{product_str}'")
                                    await page.select_option('#ctl00_cphBody_drpProject', product_str)
                                    print(f"Selected project/appraisal type: {product} (value: {product_str})")
                                    
                                    # Verify the selection
                                    selected_value = await page.eval_on_selector('#ctl00_cphBody_drpProject', 'el => el.value')
                                    selected_text = await page.eval_on_selector('#ctl00_cphBody_drpProject', 'el => el.options[el.selectedIndex].text')
                                    print(f"DEBUG: Actual selected value in dropdown: '{selected_value}'")
                                    print(f"DEBUG: Actual selected text in dropdown: '{selected_text}'")
                                    
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Fill date appraisal needed if provided
                                date_needed = self.variables.get('date_appraisal_needed')
                                if date_needed:
                                    await page.fill('#ctl00_cphBody_txtDateNeeded', date_needed)
                                    print(f"Filled date appraisal needed field with: {date_needed}")
                                    await page.wait_for_timeout(500)  # Reduced from 2000 to 500
                                
                                # Extract appraisal fee
                                try:
                                    appraisal_fee_element = await page.wait_for_selector('#ctl00_cphBody_lblAppraisalFee', timeout=10000)
                                    appraisal_fee = await appraisal_fee_element.text_content()
                                    print(f"Extracted appraisal fee: {appraisal_fee}")
                                    
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
                                    print(f"Error extracting appraisal fee: {e}")
                                    return {"error": f"Failed to extract appraisal fee: {str(e)}"}
                                
                            except Exception as e:
                                print(f"Error loading appraisal form: {e}")
                                return {"error": f"Failed to load appraisal form: {str(e)}"}
                                
                        except Exception as e:
                            print(f"Error loading dashboard: {e}")
                            return {"error": f"Failed to load dashboard: {str(e)}"}
                            
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
        print("Usage: python nadlan_playwright_fast.py '<json_variables>'")
        sys.exit(1)
    
    try:
        variables_json = sys.argv[1]
        print(f"DEBUG: Raw input: {variables_json}")
        
        variables = json.loads(variables_json)
        print(f"DEBUG: Parsed variables: {variables}")
        
        nadlan = NadlanPlaywrightFast(variables)
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
