#!/bin/bash

# Deploy Appraisal Price API to SSH Droplet

# Configuration - Update these variables
DROPLET_IP="167.172.17.131"
DROPLET_USER="ubuntu"
SSH_KEY_PATH="~/.ssh/id_rsa"
REMOTE_DIR="/home/$DROPLET_USER/appraisal_price_api"

echo "=== Deploying Appraisal Price API to Droplet ==="
echo "Droplet IP: $DROPLET_IP"
echo "Username: $DROPLET_USER"
echo "Remote Directory: $REMOTE_DIR"
echo ""

# Check if SSH key exists
if [ ! -f "$SSH_KEY_PATH" ]; then
    echo "Error: SSH key not found at $SSH_KEY_PATH"
    echo "Please update the SSH_KEY_PATH variable in this script"
    exit 1
fi

# Create remote directory
echo "Creating remote directory..."
ssh -i "$SSH_KEY_PATH" "$DROPLET_USER@$DROPLET_IP" "mkdir -p $REMOTE_DIR"

if [ $? -ne 0 ]; then
    echo "Error: Failed to create remote directory"
    exit 1
fi

# Copy files to droplet
echo "Copying files to droplet..."
scp -i "$SSH_KEY_PATH" \
    main.py \
    nadlan_playwright_simple_working.py \
    droplet_server.py \
    requirements.txt \
    README.md \
    "$DROPLET_USER@$DROPLET_IP:$REMOTE_DIR/"

if [ $? -ne 0 ]; then
    echo "Error: Failed to copy files to droplet"
    exit 1
fi

# Install dependencies on droplet
echo "Installing dependencies on droplet..."
ssh -i "$SSH_KEY_PATH" "$DROPLET_USER@$DROPLET_IP" "cd $REMOTE_DIR && pip3 install -r requirements.txt"

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies on droplet"
    exit 1
fi

# Install Playwright browsers on droplet
echo "Installing Playwright browsers on droplet..."
ssh -i "$SSH_KEY_PATH" "$DROPLET_USER@$DROPLET_IP" "cd $REMOTE_DIR && playwright install firefox"

if [ $? -ne 0 ]; then
    echo "Error: Failed to install Playwright browsers on droplet"
    exit 1
fi

# Test the deployment
echo "Testing deployment..."
ssh -i "$SSH_KEY_PATH" "$DROPLET_USER@$DROPLET_IP" "cd $REMOTE_DIR && python3 -c 'import playwright; print(\"Playwright installed successfully\")'"

if [ $? -ne 0 ]; then
    echo "Error: Playwright test failed on droplet"
    exit 1
fi

echo ""
echo "=== Deployment Successful ==="
echo "Files deployed to: $REMOTE_DIR"
echo ""
echo "To run the API on the droplet:"
echo "ssh -i $SSH_KEY_PATH $DROPLET_USER@$DROPLET_IP"
echo "cd $REMOTE_DIR"
echo "python3 main.py"
echo ""
echo "To run the standalone script on the droplet:"
echo "ssh -i $SSH_KEY_PATH $DROPLET_USER@$DROPLET_IP"
echo "cd $REMOTE_DIR"
echo "python3 nadlan_playwright_simple_working.py '{\"username\":\"AaronK\",\"password\":\"berlinchildhood$\",\"transaction_type\":\"Purchase\",\"property_type\":\"Single Family Residential\",\"property_address\":\"15 Burr Avenue\",\"property_city\":\"Marlboro Township\",\"property_state\":\"New Jersey\",\"property_zip\":\"07751\",\"occupancy_type\":\"Investment\",\"product\":59,\"headless\":true}'"
echo ""
echo "To run the API server on the droplet:"
echo "ssh -i $SSH_KEY_PATH $DROPLET_USER@$DROPLET_IP"
echo "cd $REMOTE_DIR"
echo "python3 droplet_server.py"
echo ""
echo "To execute via SSH from your local machine:"
echo "ssh -i $SSH_KEY_PATH $DROPLET_USER@$DROPLET_IP \"cd $REMOTE_DIR && python3 nadlan_playwright_simple_working.py '{\\\"username\\\":\\\"AaronK\\\",\\\"password\\\":\\\"berlinchildhood$\\\",\\\"transaction_type\\\":\\\"Purchase\\\",\\\"property_type\\\":\\\"Single Family Residential\\\",\\\"property_address\\\":\\\"15 Burr Avenue\\\",\\\"property_city\\\":\\\"Marlboro Township\\\",\\\"property_state\\\":\\\"New Jersey\\\",\\\"property_zip\\\":\\\"07751\\\",\\\"occupancy_type\\\":\\\"Investment\\\",\\\"product\\\":59,\\\"headless\\\":true}'\""
