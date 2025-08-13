#!/usr/bin/env python3
"""
Test Client for Appraisal Price API
This script demonstrates how to use the API endpoints
"""

import requests
import json
import time

# API base URL
API_BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_nadlan_script():
    """Test the Nadlan script endpoint"""
    print("Testing Nadlan script endpoint...")
    
    # Prepare the request data
    request_data = {
        "url": "https://nadlanvaluation.spurams.com/login.aspx",
        "variables": {
            "wait_time": 3000,
            "screenshot_path": "nadlan_test_screenshot.png",
            "headless": True
        }
    }
    
    print(f"Request data: {json.dumps(request_data, indent=2)}")
    
    # Make the request
    response = requests.post(
        f"{API_BASE_URL}/run-nadlan-script",
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['message']}")
        print(f"Result: {json.dumps(result['result'], indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_generic_playwright():
    """Test the generic Playwright endpoint"""
    print("Testing generic Playwright endpoint...")
    
    request_data = {
        "url": "https://nadlanvaluation.spurams.com/login.aspx",
        "variables": {
            "custom_wait": 2000,
            "take_screenshot": True
        },
        "script_name": "test_script"
    }
    
    print(f"Request data: {json.dumps(request_data, indent=2)}")
    
    response = requests.post(
        f"{API_BASE_URL}/run-playwright",
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['message']}")
        print(f"Result: {json.dumps(result['result'], indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_ssh_command():
    """Test the SSH command endpoint"""
    print("Testing SSH command endpoint...")
    
    # Note: This is an example - you'll need to provide real SSH credentials
    request_data = {
        "host": "your-droplet-ip",
        "username": "your-username",
        "private_key_path": "/path/to/your/private/key",
        "command": "python3 /path/to/script.py",
        "variables": {
            "script_path": "/home/user/scripts/",
            "output_file": "result.json"
        }
    }
    
    print("SSH endpoint example (not executed - requires real credentials):")
    print(f"Request data: {json.dumps(request_data, indent=2)}")
    print("To use this endpoint, update the credentials and uncomment the request below")
    print()
    
    # Uncomment the following lines when you have real SSH credentials
    """
    response = requests.post(
        f"{API_BASE_URL}/run-ssh",
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['message']}")
        print(f"Result: {json.dumps(result['result'], indent=2)}")
    else:
        print(f"Error: {response.text}")
    """

def run_standalone_nadlan_script():
    """Run the standalone Nadlan script directly"""
    print("Running standalone Nadlan script...")
    
    import subprocess
    import sys
    
    # Variables to pass to the script
    variables = {
        "target_url": "https://nadlanvaluation.spurams.com/login.aspx",
        "wait_time": 3000,
        "screenshot_path": "standalone_nadlan_screenshot.png",
        "headless": True
    }
    
    try:
        # Run the standalone script
        result = subprocess.run(
            [sys.executable, "nadlan_playwright.py", json.dumps(variables)],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("Script output:")
        print(result.stdout)
        
        if result.stderr:
            print("Script errors:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"Script failed with return code {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
    except Exception as e:
        print(f"Error running script: {e}")

def main():
    """Main function to run all tests"""
    print("=== Appraisal Price API Test Client ===\n")
    
    # Test root endpoint
    test_root_endpoint()
    
    # Test Nadlan script endpoint
    test_nadlan_script()
    
    # Test generic Playwright endpoint
    test_generic_playwright()
    
    # Test SSH command endpoint (example only)
    test_ssh_command()
    
    # Run standalone script
    print("=== Running Standalone Script ===")
    run_standalone_nadlan_script()

if __name__ == "__main__":
    main()
