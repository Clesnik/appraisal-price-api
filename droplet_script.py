#!/usr/bin/env python3
"""
Droplet Script for Nadlan Valuation Automation
This script can be deployed to your SSH droplet and executed remotely
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from playwright.async_api import async_playwright

class DropletNadlanScript:
    def __init__(self, variables=None):
        self.variables = variables or {}
        self.target_url = self.variables.get('target_url', 'https://nadlanvaluation.spurams.com/login.aspx')
        self.wait_time = self.variables.get('wait_time', 5000)
        self.screenshot_path = self.variables.get('screenshot_path', f'nadlan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        self.output_file = self.variables.get('output_file', f'result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        
    async def run(self):
        """Main execution method for droplet deployment"""
        print(f"Starting Nadlan automation at {datetime.now()}")
        print(f"Target URL: {self.target_url}")
        
        async with async_playwright() as p:
            # Use Firefox for better stability
            browser = await p.firefox.launch(headless=self.variables.get('headless', False))
            page = await browser.new_page()
            
            try:
                result = await self._process_page(page)
                
                # Save result to file
                with open(self.output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"Result saved to: {self.output_file}")
                print(f"Screenshot saved to: {self.screenshot_path}")
                
                # Print summary
                print(json.dumps(result, indent=2))
                
                return result
                
            except Exception as e:
                error_result = {
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "target_url": self.target_url
                }
                
                print(f"Error occurred: {e}")
                print(json.dumps(error_result, indent=2))
                
                # Save error to file
                with open(f'error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
                    json.dump(error_result, f, indent=2)
                
                return error_result
                
            finally:
                await browser.close()
    
    async def _process_page(self, page):
        """Process the Nadlan valuation page"""
        # Navigate to the login page
        await page.goto(self.target_url)
        
        # Wait for page to load
        await page.wait_for_load_state("networkidle")
        
        # Wait additional time if specified
        if self.wait_time > 0:
            await page.wait_for_timeout(self.wait_time)
        
        # Fill in username if provided
        username = self.variables.get('username', 'AaronK')  # Default test value
        if username:
            try:
                # Wait for username field to be available
                await page.wait_for_selector('#ctl00_cphBody_Login1_UserName', timeout=5000)
                
                # Fill in the username
                await page.fill('#ctl00_cphBody_Login1_UserName', username)
                print(f"Filled username field with: {username}")
                
                # Wait a moment for the input to register
                await page.wait_for_timeout(1000)
                
            except Exception as e:
                print(f"Error filling username: {e}")
        
        # Fill in password if provided
        password = self.variables.get('password', 'berlinchildhood$')  # Default test value
        if password:
            try:
                # Wait for password field to be available
                await page.wait_for_selector('#ctl00_cphBody_Login1_Password', timeout=5000)
                
                # Fill in the password
                await page.fill('#ctl00_cphBody_Login1_Password', password)
                print(f"Filled password field with: {password}")
                
                # Wait a moment for the input to register
                await page.wait_for_timeout(1000)
                
            except Exception as e:
                print(f"Error filling password: {e}")
        
        # Click login button if credentials are provided
        if username and password:
            try:
                # Wait for login button to be available
                await page.wait_for_selector('#ctl00_cphBody_Login1_LoginButton', timeout=5000)
                
                # Click the login button
                await page.click('#ctl00_cphBody_Login1_LoginButton')
                print("Clicked login button")
                
                # Wait for navigation to dashboard
                await page.wait_for_timeout(5000)
                
                # Wait for dashboard to load (look for dashboard elements)
                try:
                    await page.wait_for_selector('#ctl00_cphBody_btnAddAppraisal', timeout=10000)
                    print("Dashboard loaded successfully")
                    
                    # Click the "Create New Order" button
                    await page.click('#ctl00_cphBody_btnAddAppraisal')
                    print("Clicked 'Create New Order' button")
                    
                    # Wait for the new page to load
                    await page.wait_for_timeout(3000)
                    
                    # Wait for the appraisal form to load and select transaction type
                    try:
                        await page.wait_for_selector('#ctl00_cphBody_drpTransactionType', timeout=10000)
                        print("Appraisal form loaded successfully")
                        
                        # Select transaction type if provided
                        transaction_type = self.variables.get('transaction_type', 'Purchase')  # Default test value
                        if transaction_type:
                            # Map transaction type names to their values
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
                            
                            # Get the value for the transaction type
                            transaction_value = transaction_type_map.get(transaction_type, '1')  # Default to Purchase
                            
                            # Select the transaction type
                            await page.select_option('#ctl00_cphBody_drpTransactionType', transaction_value)
                            print(f"Selected transaction type: {transaction_type} (value: {transaction_value})")
                            
                            # Wait for any dynamic content to load
                            await page.wait_for_timeout(2000)
                            
                            # Select loan type if provided
                            loan_type = self.variables.get('loan_type', 'Other (please specify)')  # Default test value
                            if loan_type:
                                try:
                                    # Wait for loan type dropdown to be available
                                    await page.wait_for_selector('#ctl00_cphBody_drpLoanType', timeout=5000)
                                    
                                    # Map loan type names to their values
                                    loan_type_map = {
                                        'Conventional': '1',
                                        'VA': '2',
                                        'FHA': '3',
                                        'USDA / Rural Housing Service': '4',
                                        'Other (please specify)': '5',
                                        'List Price Determination': '6',
                                        'HARP 2': '7',
                                        'Home Equity': '8',
                                        'Home Ownership Accelerator': '9',
                                        'Jumbo': '10',
                                        'Reverse Mortgage': '11',
                                        'FHA 203K': '12',
                                        'Homestyle Renovation': '13',
                                        'Public And Indian Housing': '14',
                                        'ConvInsured': '15',
                                        'Non QM': '16',
                                        'Prime Jumbo': '17',
                                        'Non-Conforming': '18'
                                    }
                                    
                                    # Get the value for the loan type
                                    loan_value = loan_type_map.get(loan_type, '5')  # Default to Other
                                    
                                    # Select the loan type
                                    await page.select_option('#ctl00_cphBody_drpLoanType', loan_value)
                                    print(f"Selected loan type: {loan_type} (value: {loan_value})")
                                    
                                    # Wait for any postback or dynamic content to load
                                    await page.wait_for_timeout(3000)
                                    
                                    # Fill in loan number if provided
                                    loan_number = self.variables.get('loan_number', '000000')  # Default test value
                                    if loan_number:
                                        try:
                                            # Wait for loan number field to be available
                                            await page.wait_for_selector('#ctl00_cphBody_txtLoanNumber', timeout=5000)
                                            
                                            # Fill in the loan number
                                            await page.fill('#ctl00_cphBody_txtLoanNumber', loan_number)
                                            print(f"Filled loan number field with: {loan_number}")
                                            
                                            # Wait a moment for the input to register
                                            await page.wait_for_timeout(1000)
                                            
                                            # Fill in borrower name if provided
                                            borrower = self.variables.get('borrower', 'Example LLC')  # Default test value
                                            if borrower:
                                                try:
                                                    # Wait for borrower name field to be available
                                                    await page.wait_for_selector('#ctl00_cphBody_txtBorrowerName', timeout=5000)
                                                    
                                                    # Fill in the borrower name
                                                    await page.fill('#ctl00_cphBody_txtBorrowerName', borrower)
                                                    print(f"Filled borrower name field with: {borrower}")
                                                    
                                                    # Wait a moment for the input to register
                                                    await page.wait_for_timeout(1000)
                                                    
                                                    # Select property type if provided
                                                    property_type = self.variables.get('property_type', 'Single Family Residential')  # Default test value
                                                    if property_type:
                                                        try:
                                                            # Wait for property type dropdown to be available
                                                            await page.wait_for_selector('#ctl00_cphBody_drpPropertyType', timeout=5000)
                                                            
                                                            # Map property type names to their values
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
                                                            
                                                            property_value = property_type_map.get(property_type, '13')  # Default to Single Family Residential
                                                            await page.select_option('#ctl00_cphBody_drpPropertyType', property_value)
                                                            print(f"Selected property type: {property_type} (value: {property_value})")
                                                            await page.wait_for_timeout(2000)
                                                            
                                                            # Fill in property address if provided
                                                            property_address = self.variables.get('property_address', '15 Burr Avenue')  # Default test value
                                                            if property_address:
                                                                try:
                                                                    # Wait for property address field to be available
                                                                    await page.wait_for_selector('#ctl00_cphBody_txtPropertyAddress', timeout=5000)
                                                                    
                                                                    # Fill in the property address
                                                                    await page.fill('#ctl00_cphBody_txtPropertyAddress', property_address)
                                                                    print(f"Filled property address field with: {property_address}")
                                                                    
                                                                    # Wait a moment for the input to register and address verification
                                                                    await page.wait_for_timeout(2000)
                                                                    
                                                                    # Fill in property city if provided
                                                                    city = self.variables.get('city', 'Morganville')  # Default test value
                                                                    if city:
                                                                        try:
                                                                            # Wait for property city field to be available
                                                                            await page.wait_for_selector('#ctl00_cphBody_txtPropertyCity', timeout=5000)
                                                                            
                                                                            # Fill in the property city
                                                                            await page.fill('#ctl00_cphBody_txtPropertyCity', city)
                                                                            print(f"Filled property city field with: {city}")
                                                                            
                                                                            # Wait a moment for the input to register and address verification
                                                                            await page.wait_for_timeout(2000)
                                                                            
                                                                            # Select property state if provided
                                                                            property_state = self.variables.get('property_state', 'New Jersey')  # Default test value
                                                                            if property_state:
                                                                                try:
                                                                                    # Wait for property state dropdown to be available
                                                                                    await page.wait_for_selector('#ctl00_cphBody_drpPropertyState', timeout=5000)
                                                                                    
                                                                                    # Map state names to their abbreviations
                                                                                    state_map = {
                                                                                        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
                                                                                        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
                                                                                        'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
                                                                                        'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
                                                                                        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
                                                                                        'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
                                                                                        'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
                                                                                        'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
                                                                                        'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
                                                                                        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
                                                                                        'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
                                                                                        'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
                                                                                        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
                                                                                    }
                                                                                    
                                                                                    # Try to find the state value (either full name or abbreviation)
                                                                                    state_value = state_map.get(property_state, property_state)
                                                                                    
                                                                                    # Select the state
                                                                                    await page.select_option('#ctl00_cphBody_drpPropertyState', state_value)
                                                                                    print(f"Selected property state: {property_state} (value: {state_value})")
                                                                                    await page.wait_for_timeout(2000)
                                                                                    
                                                                                    # Fill in property zip if provided
                                                                                    property_zip = self.variables.get('property_zip', '07751')  # Default test value
                                                                                    if property_zip:
                                                                                        try:
                                                                                            # Wait for property zip field to be available
                                                                                            await page.wait_for_selector('#ctl00_cphBody_txtPropertyZip', timeout=5000)
                                                                                            
                                                                                            # Fill in the property zip
                                                                                            await page.fill('#ctl00_cphBody_txtPropertyZip', property_zip)
                                                                                            print(f"Filled property zip field with: {property_zip}")
                                                                                            
                                                                                            # Wait a moment for the input to register and address verification
                                                                                            await page.wait_for_timeout(2000)
                                                                                            
                                                                                            # Select occupancy type if provided
                                                                                            occupancy_type = self.variables.get('occupancy_type', 'Investment')  # Default test value
                                                                                            if occupancy_type:
                                                                                                try:
                                                                                                    # Wait for occupancy type dropdown to be available
                                                                                                    await page.wait_for_selector('#ctl00_cphBody_drpOccupiedBy', timeout=5000)
                                                                                                    
                                                                                                    # Map occupancy type names to their values
                                                                                                    occupancy_type_map = {
                                                                                                        'Investment': 'Investment',
                                                                                                        'Owner': 'Owner',
                                                                                                        'Primary Residence': 'Primaryresidence',
                                                                                                        'Primaryresidence': 'Primaryresidence',
                                                                                                        'Secondary Residence': 'Secondaryresidence',
                                                                                                        'Secondaryresidence': 'Secondaryresidence',
                                                                                                        'Tenant': 'Tenant',
                                                                                                        'Vacant': 'Vacant'
                                                                                                    }
                                                                                                    
                                                                                                    occupancy_value = occupancy_type_map.get(occupancy_type, 'Investment')
                                                                                                    await page.select_option('#ctl00_cphBody_drpOccupiedBy', occupancy_value)
                                                                                                    print(f"Selected occupancy type: {occupancy_type} (value: {occupancy_value})")
                                                                                                    await page.wait_for_timeout(2000)
                                                                                                    
                                                                                                    # Select contact person if provided
                                                                                                    contact_person = self.variables.get('contact_person', 'Agent')  # Default test value
                                                                                                    if contact_person:
                                                                                                        try:
                                                                                                            # Wait for contact person dropdown to be available
                                                                                                            await page.wait_for_selector('#ctl00_cphBody_drpAppointmentContact', timeout=5000)
                                                                                                            
                                                                                                            # Map contact person names to their values
                                                                                                            contact_person_map = {
                                                                                                                'Borrower': 'borrower',
                                                                                                                'Agent': 'agent',
                                                                                                                'Other': 'other'
                                                                                                            }
                                                                                                            
                                                                                                            contact_value = contact_person_map.get(contact_person, 'agent')
                                                                                                            await page.select_option('#ctl00_cphBody_drpAppointmentContact', contact_value)
                                                                                                            print(f"Selected contact person: {contact_person} (value: {contact_value})")
                                                                                                            await page.wait_for_timeout(2000)
                                                                                                            
                                                                                                        except Exception as e:
                                                                                                            print(f"Contact person selection failed: {e}")
                                                                                                    
                                                                                                    # Fill in access instructions if provided
                                                                                                    other_access_instructions = self.variables.get('other_access_instructions', 'None')  # Default test value
                                                                                                    if other_access_instructions:
                                                                                                        try:
                                                                                                            # Wait for access instructions field to be available
                                                                                                            await page.wait_for_selector('#ctl00_cphBody_txtAccessInformation', timeout=5000)
                                                                                                            
                                                                                                            # Fill in the access instructions
                                                                                                            await page.fill('#ctl00_cphBody_txtAccessInformation', other_access_instructions)
                                                                                                            print(f"Filled access instructions field with: {other_access_instructions}")
                                                                                                            
                                                                                                            # Wait a moment for the input to register
                                                                                                            await page.wait_for_timeout(2000)
                                                                                                            
                                                                                                            # Fill in agent name if provided
                                                                                                            agent_name = self.variables.get('agent_name', 'Chris Lesnik')  # Default test value
                                                                                                            if agent_name:
                                                                                                                try:
                                                                                                                    # Wait for agent name field to be available
                                                                                                                    await page.wait_for_selector('#ctl00_cphBody_txtAgentName', timeout=5000)
                                                                                                                    
                                                                                                                    # Fill in the agent name
                                                                                                                    await page.fill('#ctl00_cphBody_txtAgentName', agent_name)
                                                                                                                    print(f"Filled agent name field with: {agent_name}")
                                                                                                                    
                                                                                                                    # Wait a moment for the input to register
                                                                                                                    await page.wait_for_timeout(2000)
                                                                                                                    
                                                                                                                except Exception as e:
                                                                                                                    print(f"Agent name input failed: {e}")
                                                                                                    
                                                                                                            # Select project/appraisal type if provided
                                                                                                            product = self.variables.get('product', '1004/1007 (SFR & Rent Sch)')  # Default test value
                                                                                                            if product:
                                                                                                                try:
                                                                                                                    # Wait for project dropdown to be available
                                                                                                                    await page.wait_for_selector('#ctl00_cphBody_drpAppraisalType', timeout=5000)
                                                                                                                    
                                                                                                                    # Map project names to their values
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
                                                                                                                        'MFG 1004C investment(incl 1007)': '72'
                                                                                                                    }
                                                                                                                    
                                                                                                                    product_value = product_map.get(product, '59')  # Default to 1004/1007 (SFR & Rent Sch)
                                                                                                                    await page.select_option('#ctl00_cphBody_drpAppraisalType', product_value)
                                                                                                                    print(f"Selected project/appraisal type: {product} (value: {product_value})")
                                                                                                                    await page.wait_for_timeout(2000)
                                                                                                                    
                                                                                                                    # Fill in date appraisal needed if provided
                                                                                                                    date_appraisal_needed = self.variables.get('date_appraisal_needed', '08/22/2025')  # Default test value
                                                                                                                    if date_appraisal_needed:
                                                                                                                        try:
                                                                                                                            # Wait for date needed field to be available
                                                                                                                            await page.wait_for_selector('#ctl00_cphBody_txtDateNeeded', timeout=5000)
                                                                                                                            
                                                                                                                            # Fill in the date needed
                                                                                                                            await page.fill('#ctl00_cphBody_txtDateNeeded', date_appraisal_needed)
                                                                                                                            print(f"Filled date appraisal needed field with: {date_appraisal_needed}")
                                                                                                                            
                                                                                                                            # Wait a moment for the input to register
                                                                                                                            await page.wait_for_timeout(2000)
                                                                                                                            
                                                                                                                        except Exception as e:
                                                                                                                            print(f"Date appraisal needed input failed: {e}")
                                                                                                
                                                                                                            except Exception as e:
                                                                                                                print(f"Project selection failed: {e}")
                                                                                                    
                                                                                                        except Exception as e:
                                                                                                            print(f"Access instructions input failed: {e}")
                                                                                                
                                                                                                except Exception as e:
                                                                                                    print(f"Occupancy type selection failed: {e}")
                                                                                        
                                                                                        except Exception as e:
                                                                                            print(f"Property zip input failed: {e}")
                                                                                
                                                                                except Exception as e:
                                                                                    print(f"Property state selection failed: {e}")
                                                                        
                                                                        except Exception as e:
                                                                            print(f"Property city input failed: {e}")
                                                                    
                                                                except Exception as e:
                                                                    print(f"Property address input failed: {e}")
                                                            
                                                        except Exception as e:
                                                            print(f"Property type selection failed: {e}")
                                                    
                                                except Exception as e:
                                                    print(f"Borrower name input failed: {e}")
                                            
                                        except Exception as e:
                                            print(f"Loan number input failed: {e}")
                                    
                                except Exception as e:
                                    print(f"Loan type selection failed: {e}")
                            
                    except Exception as e:
                        print(f"Transaction type selection failed: {e}")
                    
                except Exception as e:
                    print(f"Dashboard navigation failed: {e}")
                
            except Exception as e:
                print(f"Error clicking login button: {e}")
        
        # Take a screenshot
        await page.screenshot(path=self.screenshot_path)
        
        # Get page information
        title = await page.title()
        
        # Analyze the page structure
        page_analysis = await self._analyze_page(page)
        
        # Check for specific elements
        element_check = await self._check_elements(page)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "url": self.target_url,
            "screenshot_path": self.screenshot_path,
            "page_analysis": page_analysis,
            "element_check": element_check,
            "variables_used": self.variables
        }
        
        return result
    
    async def _analyze_page(self, page):
        """Analyze the page structure"""
        try:
            # Get page content
            content = await page.content()
            
            # Get visible text
            text_content = await page.text_content('body')
            
            # Count elements
            element_counts = {
                "links": len(await page.query_selector_all('a')),
                "images": len(await page.query_selector_all('img')),
                "forms": len(await page.query_selector_all('form')),
                "inputs": len(await page.query_selector_all('input')),
                "buttons": len(await page.query_selector_all('button')),
                "divs": len(await page.query_selector_all('div')),
                "tables": len(await page.query_selector_all('table'))
            }
            
            return {
                "content_length": len(content),
                "text_length": len(text_content),
                "element_counts": element_counts,
                "text_preview": text_content[:1000] + "..." if len(text_content) > 1000 else text_content
            }
            
        except Exception as e:
            return {"error": f"Page analysis failed: {str(e)}"}
    
    async def _check_elements(self, page):
        """Check for specific elements on the page"""
        try:
            elements = {}
            
            # Check for login-related elements
            login_selectors = [
                'input[type="text"]',
                'input[type="password"]',
                'input[type="submit"]',
                'input[name*="user"]',
                'input[name*="pass"]',
                'input[id*="user"]',
                'input[id*="pass"]',
                'button[type="submit"]',
                'form'
            ]
            
            for selector in login_selectors:
                elements_found = await page.query_selector_all(selector)
                elements[selector] = len(elements_found)
            
            # Check for specific text content
            text_content = await page.text_content('body').lower()
            elements["has_login_text"] = "login" in text_content
            elements["has_password_text"] = "password" in text_content
            elements["has_username_text"] = "username" in text_content
            elements["has_email_text"] = "email" in text_content
            
            return elements
            
        except Exception as e:
            return {"error": f"Element check failed: {str(e)}"}

def main():
    """Main function for droplet deployment"""
    # Parse command line arguments
    variables = {}
    
    if len(sys.argv) > 1:
        try:
            variables = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Error: Invalid JSON in command line arguments")
            print("Usage: python3 droplet_script.py '{\"wait_time\": 3000}'")
            sys.exit(1)
    
    # Create and run the script
    script = DropletNadlanScript(variables)
    result = asyncio.run(script.run())
    
    return result

if __name__ == "__main__":
    main()
