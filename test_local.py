#!/usr/bin/env python3

import asyncio
import json
import sys
from nadlan_playwright_simple import NadlanPlaywright

async def test_local():
    """Test the script locally with visible browser"""
    
    # Test data matching your JSON payload
    test_variables = {
        "wait_time": 3000,
        "screenshot_path": "appraisal_fee_test.png",
        "headless": False,  # FALSE = VISIBLE BROWSER
        "username": "AaronK",
        "password": "berlinchildhood$",
        "transaction_type": "Purchase",
        "loan_type": "Other (please specify)",
        "loan_number": "000000",
        "borrower": "Example LLC",
        "property_type": "Multi Family - 2 Family",
        "property_address": "15 Burr Avenue",
        "property_city": "Morganville",
        "property_state": "New Jersey",
        "property_zip": "07751",
        "occupancy_type": "Investment",
        "contact_person": "Agent",
        "other_access_instructions": "None",
        "agent_name": "Chris Lesnik",
        "product": "1025/216 2-4 Multi-family",
        "date_appraisal_needed": "08/22/2025"
    }
    
    print("🚀 Starting local test with VISIBLE browser...")
    print(f"📋 Test variables: {json.dumps(test_variables, indent=2)}")
    
    try:
        nadlan = NadlanPlaywright(test_variables)
        result = await nadlan.run()
        
        print("✅ Script completed!")
        print(f"📊 Result: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_local())
