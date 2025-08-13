#!/usr/bin/env python3

import subprocess
import sys
import os

def force_deploy():
    """Force deploy the fixed server to the droplet"""
    
    # Configuration
    DROPLET_IP = "167.172.17.131"
    DROPLET_USER = "ubuntu"
    REMOTE_DIR = "/home/ubuntu"
    
    print("=== FORCE DEPLOYING FIXED SERVER ===")
    print(f"Droplet IP: {DROPLET_IP}")
    print(f"Username: {DROPLET_USER}")
    print("")
    
    # Copy the fixed server file to the droplet
    print("1. Copying fixed_server.py to droplet...")
    result = subprocess.run([
        "scp", 
        "fixed_server.py", 
        f"{DROPLET_USER}@{DROPLET_IP}:{REMOTE_DIR}/"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error copying file: {result.stderr}")
        return False
    
    print("✅ File copied successfully!")
    
    # Copy the script file too
    print("2. Copying nadlan_playwright_simple.py to droplet...")
    result = subprocess.run([
        "scp", 
        "nadlan_playwright_simple.py", 
        f"{DROPLET_USER}@{DROPLET_IP}:{REMOTE_DIR}/"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error copying script: {result.stderr}")
        return False
    
    print("✅ Script copied successfully!")
    
    # Kill any existing server processes
    print("3. Killing existing server processes...")
    kill_commands = [
        f"ssh {DROPLET_USER}@{DROPLET_IP} 'pkill -f droplet_server.py'",
        f"ssh {DROPLET_USER}@{DROPLET_IP} 'pkill -f fixed_server.py'",
        f"ssh {DROPLET_USER}@{DROPLET_IP} 'sudo lsof -t -i:8000 | xargs -r sudo kill -9'"
    ]
    
    for cmd in kill_commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: {cmd} returned {result.returncode}")
    
    print("✅ Server processes killed!")
    
    # Start the new server
    print("4. Starting the new fixed server...")
    start_cmd = f"ssh {DROPLET_USER}@{DROPLET_IP} 'cd {REMOTE_DIR} && source nadlan_env/bin/activate && nohup python3 fixed_server.py > server.log 2>&1 &'"
    
    result = subprocess.run(start_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error starting server: {result.stderr}")
        return False
    
    print("✅ Server started!")
    
    # Wait a moment for server to start
    print("5. Waiting for server to start...")
    import time
    time.sleep(3)
    
    # Test the server
    print("6. Testing the server...")
    test_cmd = f"curl -X POST 'http://{DROPLET_IP}:8000/run-appraisal' -H 'Content-Type: application/json' -d '{{\"wait_time\": 3000, \"screenshot_path\": \"test.png\", \"headless\": true, \"username\": \"test\", \"password\": \"test\", \"transaction_type\": \"Purchase\", \"loan_type\": \"Other\", \"loan_number\": \"000000\", \"borrower\": \"Test\", \"property_type\": \"Multi Family\", \"property_address\": \"123 Test St\", \"property_city\": \"Test City\", \"property_state\": \"NJ\", \"property_zip\": \"12345\", \"occupancy_type\": \"Investment\", \"contact_person\": \"Agent\", \"other_access_instructions\": \"None\", \"agent_name\": \"Test Agent\", \"product\": 2, \"date_appraisal_needed\": \"2025-01-01\"}}'"
    
    result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
    print(f"Test response: {result.stdout}")
    
    print("")
    print("=== DEPLOYMENT COMPLETE ===")
    print("The server should now accept integers for the product field.")
    print("Try your Postman request again with 'product': 2")
    
    return True

if __name__ == "__main__":
    force_deploy()
