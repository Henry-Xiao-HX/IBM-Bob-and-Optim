#!/bin/bash
# Launch script for IBM Optim Archive BI Dashboard

# Change to the dashboard directory first
cd "$(dirname "$0")"

echo "=========================================="
echo "  IBM Optim Archive - BI Dashboard"
echo "=========================================="
echo ""

# Check if .env file exists in parent directory
if [ ! -f "../.env" ]; then
    echo "❌ Error: .env file not found in parent directory"
    echo "Please create a .env file with your Optim API credentials"
    echo ""
    echo "Example .env file:"
    echo "OPTIM_BASE_URL=https://your-server:7725/optim"
    echo "OPTIM_USERNAME=your_username"
    echo "OPTIM_PASSWORD=your_password"
    exit 1
fi

echo "✅ Configuration found"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 detected"
echo ""

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "✅ Dependencies installed"
fi

echo ""
echo "🚀 Starting dashboard server..."
echo ""
echo "📊 Dashboard will be available at: http://localhost:5001"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo ""

# Run the dashboard server
python3 dashboard_server.py
