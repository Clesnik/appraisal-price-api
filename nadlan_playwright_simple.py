import asyncio
import json
import sys
from playwright.async_api import async_playwright
from datetime import datetime

class NadlanPlaywright:
    def __init__(self, variables):
        self.variables = variables
        self.target_url = variables.get('target_url', 'https://nadlanvaluation.spurams.com/login.aspx')
        self.screenshot_path = variables.get('screenshot_path', 'nadlan_screenshot.png')
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
                
                # Wait additional time if specified
                wait_time = self.variables.get('wait_time', 5000)
                if wait_time > 0:
                    await page.wait_for_timeout(wait_time)
                
                # Fill in username if provided
                username = self.variables.get('username')
                if username:
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_UserName', timeout=5000)
                        await page.fill('#ctl00_cphBody_Login1_UserName', username)
                        print(f"Filled username field with: {username}")
                        await page.wait_for_timeout(1000)
                    except Exception as e:
                        print(f"Error filling username: {e}")
                
                # Fill in password if provided
                password = self.variables.get('password')
                if password:
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_Password', timeout=5000)
                        await page.fill('#ctl00_cphBody_Login1_Password', password)
                        print(f"Filled password field with: {password}")
                        await page.wait_for_timeout(1000)
                    except Exception as e:
                        print(f"Error filling password: {e}")
                
                # Click login button if credentials are provided
                if username and password:
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_Login1_LoginButton', timeout=5000)
                        await page.click('#ctl00_cphBody_Login1_LoginButton')
                        print("Clicked login button")
                        await page.wait_for_timeout(5000)
                        
                        # Wait for dashboard to load
                        try:
                            await page.wait_for_selector('#ctl00_cphBody_btnAddAppraisal', timeout=10000)
                            print("Dashboard loaded successfully")
                            
                            # Click the "Create New Order" button
                            await page.click('#ctl00_cphBody_btnAddAppraisal')
                            print("Clicked 'Create New Order' button")
                            await page.wait_for_timeout(3000)
                            
                            # Wait for the appraisal form to load
                            try:
                                await page.wait_for_selector('#ctl00_cphBody_drpTransactionType', timeout=10000)
                                print("Appraisal form loaded successfully")
                                
                                # Select transaction type if provided
                                transaction_type = self.variables.get('transaction_type')
                                if transaction_type:
                                    transaction_type_map = {
                                        'Purchase': '1',
                                        'Refinance': '2',
                                        'Market Value': '15',
                                        'Reverse Mortgage': '16',
                                        'List Price Determination': '17',
                                        'Home Equity Line of Credit': '18',
                                        'Market Value for Lender Purposes': '19',
                                        'FHA': '21',
                                        'Construction': '23',
                                        'Second Mortgage': '24',
                                        'Acquisition': '27',
                                        'HELOC': '34',
                                        'Investment Property': '9',
                                        'Other': '14'
                                    }
                                    transaction_value = transaction_type_map.get(transaction_type, '1')
                                    await page.select_option('#ctl00_cphBody_drpTransactionType', transaction_value)
                                    print(f"Selected transaction type: {transaction_type} (value: {transaction_value})")
                                    await page.wait_for_timeout(2000)
                                
                                # Select loan type if provided
                                loan_type = self.variables.get('loan_type')
                                if loan_type:
                                    loan_type_map = {
                                        'Conventional': '1',
                                        'FHA': '2',
                                        'VA': '3',
                                        'USDA': '4',
                                        'Other (please specify)': '5'
                                    }
                                    loan_value = loan_type_map.get(loan_type, '5')
                                    await page.select_option('#ctl00_cphBody_drpLoanType', loan_value)
                                    print(f"Selected loan type: {loan_type} (value: {loan_value})")
                                    await page.wait_for_timeout(2000)
                                
                                # Fill in loan number if provided
                                loan_number = self.variables.get('loan_number')
                                if loan_number:
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtLoanNumber', timeout=5000)
                                        await page.fill('#ctl00_cphBody_txtLoanNumber', loan_number)
                                        print(f"Filled loan number field with: {loan_number}")
                                        await page.wait_for_timeout(2000)
                                    except Exception as e:
                                        print(f"Loan number input failed: {e}")
                                
                                # Fill in borrower name if provided
                                borrower = self.variables.get('borrower')
                                if borrower:
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtBorrowerName', timeout=5000)
                                        await page.fill('#ctl00_cphBody_txtBorrowerName', borrower)
                                        print(f"Filled borrower name field with: {borrower}")
                                        await page.wait_for_timeout(2000)
                                    except Exception as e:
                                        print(f"Borrower name input failed: {e}")
                                
                                # Select property type if provided
                                property_type = self.variables.get('property_type')
                                if property_type:
                                    property_type_map = {
                                        'Single Family Residential': '13',
                                        'Condo': '14',
                                        'Townhouse': '15',
                                        'Multi-Family': '16',
                                        'Multi Family - 2 Family': '16',
                                        'Commercial': '17',
                                        'Land': '18',
                                        'Other': '19'
                                    }
                                    property_value = property_type_map.get(property_type, '13')
                                    await page.select_option('#ctl00_cphBody_drpPropertyType', property_value)
                                    print(f"Selected property type: {property_type} (value: {property_value})")
                                    await page.wait_for_timeout(2000)
                                
                                # Fill in property address if provided
                                property_address = self.variables.get('property_address')
                                if property_address:
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtPropertyAddress', timeout=5000)
                                        await page.fill('#ctl00_cphBody_txtPropertyAddress', property_address)
                                        print(f"Filled property address field with: {property_address}")
                                        await page.wait_for_timeout(2000)
                                    except Exception as e:
                                        print(f"Property address input failed: {e}")
                                
                                # Fill in property city if provided
                                property_city = self.variables.get('property_city')
                                if property_city:
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtPropertyCity', timeout=5000)
                                        await page.fill('#ctl00_cphBody_txtPropertyCity', property_city)
                                        print(f"Filled property city field with: {property_city}")
                                        await page.wait_for_timeout(2000)
                                    except Exception as e:
                                        print(f"Property city input failed: {e}")
                                
                                # Select property state if provided
                                property_state = self.variables.get('property_state')
                                if property_state:
                                    property_state_map = {
                                        'New Jersey': 'NJ',
                                        'New York': 'NY',
                                        'California': 'CA',
                                        'Texas': 'TX',
                                        'Florida': 'FL'
                                    }
                                    state_value = property_state_map.get(property_state, 'NJ')
                                    await page.select_option('#ctl00_cphBody_drpPropertyState', state_value)
                                    print(f"Selected property state: {property_state} (value: {state_value})")
                                    await page.wait_for_timeout(2000)
                                
                                # Fill in property zip if provided
                                property_zip = self.variables.get('property_zip')
                                if property_zip:
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtPropertyZip', timeout=5000)
                                        await page.fill('#ctl00_cphBody_txtPropertyZip', property_zip)
                                        print(f"Filled property zip field with: {property_zip}")
                                        await page.wait_for_timeout(2000)
                                    except Exception as e:
                                        print(f"Property zip input failed: {e}")
                                
                                # Select occupancy type if provided
                                occupancy_type = self.variables.get('occupancy_type')
                                if occupancy_type:
                                    occupancy_type_map = {
                                        'Owner Occupied': 'Owner Occupied',
                                        'Investment': 'Investment',
                                        'Second Home': 'Second Home'
                                    }
                                    occupancy_value = occupancy_type_map.get(occupancy_type, 'Investment')
                                    await page.select_option('#ctl00_cphBody_drpOccupiedBy', occupancy_value)
                                    print(f"Selected occupancy type: {occupancy_type} (value: {occupancy_value})")
                                    await page.wait_for_timeout(2000)
                                
                                # Select contact person if provided
                                contact_person = self.variables.get('contact_person')
                                if contact_person:
                                    contact_person_map = {
                                        'Agent': 'agent',
                                        'Owner': 'owner',
                                        'Tenant': 'tenant',
                                        'Property Manager': 'property_manager'
                                    }
                                    contact_value = contact_person_map.get(contact_person, 'agent')
                                    await page.select_option('#ctl00_cphBody_drpAppointmentContact', contact_value)
                                    print(f"Selected contact person: {contact_person} (value: {contact_value})")
                                    await page.wait_for_timeout(2000)
                                
                                # Fill in access instructions if provided
                                other_access_instructions = self.variables.get('other_access_instructions')
                                if other_access_instructions:
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtAccessInformation', timeout=5000)
                                        await page.fill('#ctl00_cphBody_txtAccessInformation', other_access_instructions)
                                        print(f"Filled access instructions field with: {other_access_instructions}")
                                        await page.wait_for_timeout(2000)
                                    except Exception as e:
                                        print(f"Access instructions input failed: {e}")
                                
                                # Fill in agent name if provided
                                agent_name = self.variables.get('agent_name')
                                if agent_name:
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtAgentName', timeout=5000)
                                        await page.fill('#ctl00_cphBody_txtAgentName', agent_name)
                                        print(f"Filled agent name field with: {agent_name}")
                                        await page.wait_for_timeout(2000)
                                    except Exception as e:
                                        print(f"Agent name input failed: {e}")
                                
                                # Select project/appraisal type if provided
                                product = self.variables.get('product')
                                if product:
                                    product_map = {
                                        '1004/1007 (SFR & Rent Sch)': '59',
                                        '1004 (SFR)': '1',
                                        '1007 (Rent Schedule)': '2',
                                        '1025 (Small Residential Income)': '3',
                                        '1025/216 2-4 Multi-family': '58',
                                        '1073 (Condominium)': '4',
                                        '2055 (Exterior Only)': '5'
                                    }
                                    product_value = product_map.get(product, '59')
                                    await page.select_option('#ctl00_cphBody_drpAppraisalType', product_value)
                                    print(f"Selected project/appraisal type: {product} (value: {product_value})")
                                    await page.wait_for_timeout(2000)
                                
                                # Fill in date appraisal needed if provided
                                date_appraisal_needed = self.variables.get('date_appraisal_needed')
                                if date_appraisal_needed:
                                    try:
                                        await page.wait_for_selector('#ctl00_cphBody_txtDateNeeded', timeout=5000)
                                        await page.fill('#ctl00_cphBody_txtDateNeeded', date_appraisal_needed)
                                        print(f"Filled date appraisal needed field with: {date_appraisal_needed}")
                                        await page.wait_for_timeout(2000)
                                    except Exception as e:
                                        print(f"Date appraisal needed input failed: {e}")
                                
                                # Extract appraisal fee value
                                appraisal_fee = None
                                appraisal_fee_screenshot = None
                                full_page_screenshot = None
                                try:
                                    # Wait for the appraisal fee element to be available
                                    await page.wait_for_selector('#ctl00_cphBody_lblLenderAppraisalFee', timeout=10000)
                                    
                                    # Wait for the dynamic content to load
                                    await page.wait_for_timeout(3000)
                                    
                                    # Get the appraisal fee using JavaScript to access ::before pseudo-element
                                    appraisal_fee = await page.evaluate('''
                                        () => {
                                            const element = document.querySelector('#ctl00_cphBody_lblLenderAppraisalFee');
                                            if (!element) return null;
                                            
                                            // Method 1: Get the ::before pseudo-element content
                                            const beforeStyle = window.getComputedStyle(element, '::before');
                                            const beforeContent = beforeStyle.getPropertyValue('content');
                                            
                                            console.log('Before content:', beforeContent);
                                            
                                            // Method 2: Get the full displayed text
                                            const fullText = element.innerText || element.textContent;
                                            console.log('Full text:', fullText);
                                            
                                            // Method 3: Get the computed text content
                                            const computedText = element.textContent;
                                            console.log('Computed text:', computedText);
                                            
                                            // Method 4: Try to get the actual displayed value by combining
                                            if (beforeContent && beforeContent !== 'none' && beforeContent !== 'normal') {
                                                // Remove quotes from beforeContent
                                                const cleanBeforeContent = beforeContent.replace(/['"]/g, '');
                                                console.log('Clean before content:', cleanBeforeContent);
                                                
                                                // If beforeContent has the number, combine with dollar sign
                                                if (cleanBeforeContent.match(/\\d+/)) {
                                                    return '$' + cleanBeforeContent;
                                                }
                                            }
                                            
                                            // Method 5: Try to extract from the full text
                                            if (fullText && fullText.includes('$')) {
                                                const match = fullText.match(/\\$\\d+/);
                                                if (match) {
                                                    return match[0];
                                                }
                                            }
                                            
                                            // Method 6: Get the actual rendered text
                                            const range = document.createRange();
                                            range.selectNodeContents(element);
                                            const renderedText = range.toString();
                                            console.log('Rendered text:', renderedText);
                                            
                                            return renderedText || fullText || computedText;
                                        }
                                    ''')
                                    
                                    print(f"Extracted appraisal fee: {appraisal_fee}")
                                    
                                    # Take a screenshot of the appraisal fee element for debugging
                                    try:
                                        fee_element = await page.query_selector('#ctl00_cphBody_lblLenderAppraisalFee')
                                        if fee_element:
                                            # Take screenshot of just the appraisal fee element
                                            await fee_element.screenshot(path='appraisal_fee_element.png')
                                            print("Screenshot of appraisal fee element saved as: appraisal_fee_element.png")
                                            
                                            # Also take a screenshot of the entire page for context
                                            await page.screenshot(path='full_page_appraisal_fee.png')
                                            print("Full page screenshot saved as: full_page_appraisal_fee.png")
                                            
                                            # Add screenshot paths to the result
                                            appraisal_fee_screenshot = 'appraisal_fee_element.png'
                                            full_page_screenshot = 'full_page_appraisal_fee.png'
                                        else:
                                            print("Could not find appraisal fee element for screenshot")
                                            appraisal_fee_screenshot = None
                                            full_page_screenshot = None
                                    except Exception as screenshot_error:
                                        print(f"Screenshot failed: {screenshot_error}")
                                        appraisal_fee_screenshot = None
                                        full_page_screenshot = None
                                        
                                except Exception as e:
                                    print(f"Appraisal fee extraction failed: {e}")
                                    appraisal_fee_screenshot = None
                                    full_page_screenshot = None
                                
                            except Exception as e:
                                print(f"Appraisal form loading failed: {e}")
                        
                        except Exception as e:
                            print(f"Dashboard navigation failed: {e}")
                    
                    except Exception as e:
                        print(f"Error clicking login button: {e}")
                
                # Take a screenshot
                await page.screenshot(path=self.screenshot_path)
                
                # Get page information
                title = await page.title()
                
                # Analyze the form
                form_analysis = await self._analyze_form(page)
                
                result = {
                    "appraisal_fee": appraisal_fee,
                    "appraisal_fee_screenshot": appraisal_fee_screenshot,
                    "full_page_screenshot": full_page_screenshot
                }
                
                return result
                
            except Exception as e:
                print(f"Error: {e}")
                return {"error": str(e)}
            
            finally:
                await browser.close()
    
    async def _analyze_form(self, page):
        """Analyze the form structure"""
        try:
            forms = await page.query_selector_all('form')
            form_count = len(forms)
            
            form_analysis = {
                "form_count": form_count,
                "forms": []
            }
            
            for i, form in enumerate(forms):
                form_info = await self._get_form_info(form, i)
                form_analysis["forms"].append(form_info)
            
            return form_analysis
            
        except Exception as e:
            return {"error": f"Form analysis failed: {str(e)}"}
    
    async def _get_form_info(self, form, index):
        """Get detailed information about a form"""
        try:
            action = await form.get_attribute('action')
            method = await form.get_attribute('method')
            form_id = await form.get_attribute('id')
            form_class = await form.get_attribute('class')
            
            inputs = await form.query_selector_all('input')
            input_fields = []
            
            for input_elem in inputs:
                input_type = await input_elem.get_attribute('type')
                input_name = await input_elem.get_attribute('name')
                input_id = await input_elem.get_attribute('id')
                placeholder = await input_elem.get_attribute('placeholder')
                required = await input_elem.get_attribute('required')
                
                input_fields.append({
                    "type": input_type,
                    "name": input_name,
                    "id": input_id,
                    "placeholder": placeholder,
                    "required": required is not None
                })
            
            return {
                "index": index,
                "action": action,
                "method": method,
                "id": form_id,
                "class": form_class,
                "input_fields": input_fields,
                "input_count": len(input_fields)
            }
            
        except Exception as e:
            return {"error": f"Form info extraction failed: {str(e)}"}

async def main():
    if len(sys.argv) != 2:
        print("Usage: python nadlan_playwright_simple.py '{\"variables\": \"here\"}'")
        return
    
    try:
        # Parse the JSON input
        input_data = json.loads(sys.argv[1])
        
        # Variables are passed directly
        variables = input_data
        
        print(f"DEBUG: Raw input: {sys.argv[1]}")
        print(f"DEBUG: Parsed variables: {variables}")
        
        nadlan = NadlanPlaywright(variables)
        result = await nadlan.run()
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    asyncio.run(main())
