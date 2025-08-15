#!/bin/bash

# Update Droplet Script
# This script copies the latest files to the droplet and restarts the server

DROPLET_IP="167.172.17.131"
DROPLET_USER="ubuntu"
REMOTE_DIR="/home/ubuntu/appraisal_price_api"

echo "=== Updating Appraisal Price API on Droplet ==="
echo "Droplet IP: $DROPLET_IP"
echo "Username: $DROPLET_USER"
echo "Remote Directory: $REMOTE_DIR"

# Copy the working script to the droplet
echo "📁 Copying nadlan_playwright_simple_working.py to droplet..."
scp nadlan_playwright_simple_working.py $DROPLET_USER@$DROPLET_IP:$REMOTE_DIR/

# Copy the droplet server
echo "📁 Copying droplet_server.py to droplet..."
scp droplet_server.py $DROPLET_USER@$DROPLET_IP:$REMOTE_DIR/

# Copy requirements file if it exists
if [ -f "requirements.txt" ]; then
    echo "📁 Copying requirements.txt to droplet..."
    scp requirements.txt $DROPLET_USER@$DROPLET_IP:$REMOTE_DIR/
fi

# SSH into the droplet and restart the server
echo "🔄 Connecting to droplet to restart server..."
ssh $DROPLET_USER@$DROPLET_IP << 'EOF'
    cd /home/ubuntu/appraisal_price_api
    
    # Kill any existing server processes
    echo "🛑 Stopping existing server processes..."
    pkill -f "droplet_server.py" || true
    pkill -f "fixed_server.py" || true
    
    # Wait a moment for processes to stop
    sleep 2
    
    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    # Install any new requirements
    if [ -f "requirements.txt" ]; then
        echo "📦 Installing requirements..."
        pip install -r requirements.txt
    fi
    
    # Start the server in the background
    echo "🚀 Starting server in background..."
    nohup python3 droplet_server.py > server.log 2>&1 &
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if server is running
    if pgrep -f "droplet_server.py" > /dev/null; then
        echo "✅ Server started successfully!"
        echo "📋 Server process info:"
        ps aux | grep droplet_server.py | grep -v grep
        echo "📄 Server log (last 10 lines):"
        tail -10 server.log
    else
        echo "❌ Server failed to start!"
        echo "📄 Server log:"
        cat server.log
    fi
EOF

echo "✅ Droplet update completed!"
echo "🌐 Server should be available at: http://$DROPLET_IP:8000"
echo "📋 API docs: http://$DROPLET_IP:8000/docs"
