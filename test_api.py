#!/usr/bin/env python3

import requests
import json

def test_api():
    """Test the API with different product values"""
    
    url = "http://167.172.17.131:8000/run-appraisal"
    
    # Test data
    test_data = {
        "wait_time": 3000,
        "screenshot_path": "test.png",
        "headless": True,
        "username": "test",
        "password": "test",
        "transaction_type": "Purchase",
        "loan_type": "Other",
        "loan_number": "000000",
        "borrower": "Test",
        "property_type": "Multi Family",
        "property_address": "123 Test St",
        "property_city": "Test City",
        "property_state": "NJ",
        "property_zip": "12345",
        "occupancy_type": "Investment",
        "contact_person": "Agent",
        "other_access_instructions": "None",
        "agent_name": "Test Agent",
        "date_appraisal_needed": "2025-01-01"
    }
    
    print("Testing API with different product values...")
    
    # Test 1: Integer product
    test_data["product"] = 2
    print(f"\n1. Testing with product = {test_data['product']} (integer)")
    try:
        response = requests.post(url, json=test_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: String product
    test_data["product"] = "2"
    print(f"\n2. Testing with product = '{test_data['product']}' (string)")
    try:
        response = requests.post(url, json=test_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
