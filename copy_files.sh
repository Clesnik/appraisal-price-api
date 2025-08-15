#!/bin/bash

echo "=== Copying files to droplet ==="
echo "You will be prompted for the password for each file."

# Copy the working script
scp nadlan_playwright_simple_working.py ubuntu@167.172.17.131:/home/ubuntu/appraisal_price_api/

# Copy the server
scp droplet_server.py ubuntu@167.172.17.131:/home/ubuntu/appraisal_price_api/

# Copy requirements
scp requirements.txt ubuntu@167.172.17.131:/home/ubuntu/appraisal_price_api/

echo "✅ Files copied successfully!"
echo "Now SSH into the droplet and run the server manually:"
echo "ssh ubuntu@167.172.17.131"
echo "cd /home/ubuntu/appraisal_price_api"
echo "source venv/bin/activate"
echo "nohup python3 droplet_server.py > server.log 2>&1 &"
