import asyncio
import json
import sys
from playwright.async_api import async_playwright
from datetime import datetime

class NadlanPlaywright:
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
                                    await page.wait_for_timeout(2000)
                                
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
                                        'Attached': '2',
                                        'Co-Operative (Co-Op)': '5',
                                        'Commercial Condo': '19',
                                        'Commercial/Non-residential': '15',
                                        'Condominium': '3',
                                        'Detached': '1',
                                        'Detached Condo': '8',
                                        'High-rise Condo': '6',
                                        'Land': '16',
                                        'Manufactured Home': '7',
                                        'Manufactured Home: Condo/PUD/Co-Op': '9',
                                        'MH Select': '10',
                                        'Mixed Use': '11',
                                        'Mobile Home': '18',
                                        'Multi Family - 2 Family': '12',
                                        'Multi Family - 3 Family': '20',
                                        'Multi Family - 4 Family': '21',
                                        'Planned Unit Development (PUD)': '4',
                                        'Rural': '14',
                                        'Single Family Residential': '13',
                                        'Townhome': '17'
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
                                        'Alabama': 'AL',
                                        'Alaska': 'AK',
                                        'Arizona': 'AZ',
                                        'Arkansas': 'AR',
                                        'California': 'CA',
                                        'Colorado': 'CO',
                                        'Connecticut': 'CT',
                                        'Delaware': 'DE',
                                        'District of Columbia': 'DC',
                                        'Florida': 'FL',
                                        'Georgia': 'GA',
                                        'Hawaii': 'HI',
                                        'Idaho': 'ID',
                                        'Illinois': 'IL',
                                        'Indiana': 'IN',
                                        'Iowa': 'IA',
                                        'Kansas': 'KS',
                                        'Kentucky': 'KY',
                                        'Louisiana': 'LA',
                                        'Maine': 'ME',
                                        'Maryland': 'MD',
                                        'Massachusetts': 'MA',
                                        'Michigan': 'MI',
                                        'Minnesota': 'MN',
                                        'Mississippi': 'MS',
                                        'Missouri': 'MO',
                                        'Montana': 'MT',
                                        'Nebraska': 'NE',
                                        'Nevada': 'NV',
                                        'New Hampshire': 'NH',
                                        'New Jersey': 'NJ',
                                        'New Mexico': 'NM',
                                        'New York': 'NY',
                                        'North Carolina': 'NC',
                                        'North Dakota': 'ND',
                                        'Ohio': 'OH',
                                        'Oklahoma': 'OK',
                                        'Oregon': 'OR',
                                        'Pennsylvania': 'PA',
                                        'Rhode Island': 'RI',
                                        'South Carolina': 'SC',
                                        'South Dakota': 'SD',
                                        'Tennessee': 'TN',
                                        'Texas': 'TX',
                                        'UTAH': 'UT',
                                        'Vermont': 'VT',
                                        'Virginia': 'VA',
                                        'Washington': 'WA',
                                        'West Virginia': 'WV',
                                        'Wisconsin': 'WI',
                                        'Wyoming': 'WY'
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
                                        'Investment': 'Investment',
                                        'Owner': 'Owner',
                                        'Primaryresidence': 'Primaryresidence',
                                        'Secondaryresidence': 'Secondaryresidence',
                                        'Tenant': 'Tenant',
                                        'Vacant': 'Vacant'
                                    }
                                    occupancy_value = occupancy_type_map.get(occupancy_type, 'Investment')
                                    await page.select_option('#ctl00_cphBody_drpOccupiedBy', occupancy_value)
                                    print(f"Selected occupancy type: {occupancy_type} (value: {occupancy_value})")
                                    await page.wait_for_timeout(2000)
                                
                                # Select contact person if provided
                                contact_person = self.variables.get('contact_person')
                                if contact_person:
                                    contact_person_map = {
                                        'Borrower': 'borrower',
                                        'Agent': 'agent',
                                        'Other': 'other'
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
                                        '1004 Single Family': '1',
                                        '1004/1007 (SFR & Rent Sch)': '59',
                                        '1004/1007/216': '58',
                                        '1004 & 216 (SFR & Op. Income)': '86',
                                        '1073 Condo': '3',
                                        '1073/1007 (Condo & Rent Sch)': '55',
                                        '1073/1007/216': '56',
                                        '1073 and 216 (Condo & Op. Income)': '87',
                                        '1025 Multi Family w/out 216': '96',
                                        '1025/216 2-4 Multi-family': '2',
                                        'Homestyle 2-4 family 1025/216': '77',
                                        '1025/216 2-4 family 203K': '78',
                                        '1025/216 2-4 family USDA': '76',
                                        '1004C Manufactured Home': '19',
                                        'MFG 1004C investment(incl 1007)': '72',
                                        '2098 Cooperative': '26',
                                        'FHA 1004 Single Family': '22',
                                        'FHA 1004/1007 (SFR & Rent Sch)': '63',
                                        'FHA 1004/1007/216': '57',
                                        'FHA 1073 Condo': '25',
                                        'FHA 1073/1007/216': '54',
                                        'FHA 1025 Multi Family w/out 216': '95',
                                        'FHA 1025/216 2-4 Multi-family': '24',
                                        'FHA 2098 Cooperative': '27',
                                        'MFG 1004C FHA': '71',
                                        'FHA Appraisal (FNMA 1004)': '93',
                                        'FHA Conversion Appraisal Update': '51',
                                        'FHA Converted to Conventional': '61',
                                        'USDA Appraisal (FNMA 1004)': '94',
                                        'Rush Fee': '62',
                                        'Rural/Remote Fee': '79',
                                        'Property Value 1M+': '37',
                                        'Complex Property': '89',
                                        'Final Inspection 1004D': '33',
                                        'RECERTIFICATION OF VALUE /APPRAISAL UPDATE 1004D': '23',
                                        '1004D Combo (Final Inspect + Recert)': '85',
                                        'CDAIR Disaster Report': '88',
                                        'FHA Inspection (CIR)': '42',
                                        '1007 Rent Comparables': '28',
                                        '216 Income Statement': '29',
                                        '216 and 1007': '65',
                                        '1033 Desk Review': '18',
                                        '1075 Condo Exterior Only': '5',
                                        '2000 Field Review': '17',
                                        '2055 Exterior Only': '4',
                                        '2070 Condition and Marketability Report': '38',
                                        '2075 DU Property Inspection': '38',
                                        '2095 Exterior Only Cooperative': '40',
                                        'Retro Field Review': '50',
                                        'ACE+PDR': '116',
                                        'BPO Desktop': '117',
                                        'BPO Exterior': '118',
                                        'BPO Interior': '119',
                                        'Condo 203K': '75',
                                        'Uniform Residential Appraisal Report Desktop (1004 Desktop/780)': '108',
                                        'Uniform Residential Appraisal Report Hybrid (1004 Hybrid/70H)': '109',
                                        '1004 As Is Value ARV & 1007': '107',
                                        '1004 As Is Value ARV': '113',
                                        '1025 As Is Value ARV (Without 216)': '114',
                                        '71A': '101',
                                        '718': '102',
                                        '718 Mixed Use': '53',
                                        'General Purpose': '103',
                                        'Summary/Narrative Report': '184',
                                        'Summary/Narrative Report Format': '110',
                                        'Bulk Product': '105',
                                        'Commercial Product': '106',
                                        'Jumbo 1004': '92',
                                        'Jumbo 1025/216 MF': '91',
                                        'Jumbo 1073': '90',
                                        'Homestyle Condo 1073': '74',
                                        'Condo USDA': '73',
                                        'Covid Desktop 1004': '84',
                                        'Covid FHA 1004 Exterior': '83',
                                        'AVM': '16',
                                        'Desktop Quantitative Appraisal': '49',
                                        'Desktop Summary Appraisal': '48',
                                        'NDR (1004D form)': '31',
                                        'FNM 10040 Final Inspection': '13',
                                        'FHA Field Review (HUD 1038)': '41',
                                        'Questionnaire Fee': '52',
                                        'HomeStyle Renovation 1004': '64',
                                        'Reverse FHA 1004 SFR': '45',
                                        'Single Family 203K': '69',
                                        'Single family USDA': '78',
                                        'FHA 203K Conversion Update': '68',
                                        '1004 Homesafe Appraisal': '97',
                                        '1025 Homesafe Appraisal': '98',
                                        '1073 Homesafe Appraisal': '99',
                                        'Employee Relocation Council Report (ERC)': '39',
                                        'Farm Land/Owner Occupied': '34',
                                        'General Purpose Appraisal Report GPAR': '68',
                                        'Standard Fee for the Area': '81',
                                        'Supplemental REO Addendum': '46',
                                        'Vacant Land Report': '6',
                                        'Vacating/Departure Appraisal Report': '36',
                                        'FNMA 1081': '115',
                                        'CDAIR': '82',
                                        'Appeal/Reconsideration of Value': '88',
                                        'Revision': '66',
                                        'Chargeback/Bounced Check Fee': '67',
                                        'Trip Fee': '32',
                                        'CIR Compliance Inspection 92051': '120',
                                        'Construction Draw': '121',
                                        'FNMA Value Acceptance Property Data': '122',
                                        '2000A 2-4 Family Field Review': '126',
                                        '1073 As Is Value ARV & 1007': '127',
                                        '71 A/B Form': '100',
                                        '1073 As Is Value ARV': '128',
                                        'URAR Hybrid (1073 Hybrid/70H)': '129',
                                        '1004P': '130',
                                        'HomeStyle Renovation 1004/1007 Investment': '132',
                                        'Property Completion Report (PCR Hybrid)': '133',
                                        '2055 Exterior Only Multi-Family': '134',
                                        'CDA w MLS Sheets': '139',
                                        'CDA w/o MLS Sheets': '140',
                                        'Completion Report - PDC Exterior': '141',
                                        'Completion Report - PDC Interior': '142',
                                        'USDA 1004D': '145',
                                        'DAIR - Exterior': '146',
                                        '1025 Comparable Rental Data Only': '147',
                                        'Jumbo (1004 and 1007)': '148',
                                        'Internal ENV Report Only': '149',
                                        'Short Term Rental Rent Schedule Narrative': '150',
                                        '1025 As Is Value ARV with a 216': '151',
                                        '1004 & Short Term Rental Rent Schedule Narrative': '152',
                                        '1073 & Short Term Rental Rent Schedule Narrative': '153',
                                        'New Construction (1004)': '154',
                                        'FHA New Construction (1004)': '155',
                                        'USDA Multi Family (1025)': '156',
                                        'FCM 1007 Comparable Rent Schedule +STR': '157',
                                        'FCM Single Family Investment w/1007 +STR': '158',
                                        'FCM Single Family Invest (1004, 1007, and 216)+STR': '159',
                                        'FCM Condo Invest (1073 & 1007) +STR': '160',
                                        'FCM Condo Invest (1073, 1007 & 216) + STR': '161',
                                        'FCM Manufacture Invest (1004C, 1007, 216) +STR': '162',
                                        'FCM Manufactured Invest (1004C & 1007)+STR': '163',
                                        'JUMBO FHA 203K Multi Family': '164',
                                        'eVal Exterior': '165',
                                        'eVal Interior': '166',
                                        'ValPraze Exterior': '167',
                                        'ValPraze Interior': '168'
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
                

                
                # Get page information
                title = await page.title()
                
                # Analyze the form
                form_analysis = await self._analyze_form(page)
                
                result = {
                    "appraisal_fee": appraisal_fee
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
