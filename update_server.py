#!/usr/bin/env python3

import subprocess
import sys
import os

def update_droplet_server():
    """Update the droplet server with the correct code"""
    
    # Configuration
    DROPLET_IP = "167.172.17.131"
    DROPLET_USER = "ubuntu"
    REMOTE_DIR = "/home/ubuntu/appraisal_price_api"
    
    print("=== Updating Droplet Server ===")
    print(f"Droplet IP: {DROPLET_IP}")
    print(f"Username: {DROPLET_USER}")
    print(f"Remote Directory: {REMOTE_DIR}")
    print("")
    
    # Create remote directory first
    print("Creating remote directory...")
    result = subprocess.run([
        "ssh", f"{DROPLET_USER}@{DROPLET_IP}", f"mkdir -p {REMOTE_DIR}"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error creating directory: {result.stderr}")
        return False
    
    # Copy the updated droplet_server.py to the droplet
    print("Copying updated droplet_server.py to droplet...")
    result = subprocess.run([
        "scp", 
        "droplet_server.py", 
        f"{DROPLET_USER}@{DROPLET_IP}:{REMOTE_DIR}/"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error copying file: {result.stderr}")
        return False
    
    print("File copied successfully!")
    
    # Restart the server on the droplet
    print("Restarting the server on the droplet...")
    restart_commands = [
        f"ssh {DROPLET_USER}@{DROPLET_IP} 'cd {REMOTE_DIR} && pkill -f droplet_server.py'",
        f"ssh {DROPLET_USER}@{DROPLET_IP} 'cd {REMOTE_DIR} && nohup python3 droplet_server.py > server.log 2>&1 &'"
    ]
    
    for cmd in restart_commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: {cmd} returned {result.returncode}")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
    
    print("Server restart commands sent!")
    print("")
    print("=== Update Complete ===")
    print("The server should now accept integers for the product field.")
    print("You can test it with your Postman request.")
    
    return True

if __name__ == "__main__":
    update_droplet_server()
