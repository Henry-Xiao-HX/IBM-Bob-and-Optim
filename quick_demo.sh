#!/bin/bash
# Quick Demo Launcher for IBM Optim Archive API
# Makes running demos even easier!

set -e

echo "=================================================="
echo "  IBM Optim Archive API - Quick Demo Launcher"
echo "=================================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "📝 Please edit .env and add your credentials:"
    echo "   - OPTIM_BASE_URL"
    echo "   - OPTIM_USERNAME"
    echo "   - OPTIM_PASSWORD"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if credentials are filled in
if grep -q "your_username" .env || grep -q "your_password" .env; then
    echo "⚠️  Please update .env with your actual credentials"
    echo ""
    echo "Edit .env and replace:"
    echo "   - your_username → your actual username"
    echo "   - your_password → your actual password"
    echo "   - VM_HOSTNAME → your VM hostname"
    echo ""
    exit 1
fi

echo "✅ Configuration found"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if requests module is available
if ! python3 -c "import requests" 2>/dev/null; then
    echo "📦 Installing required Python packages..."
    pip3 install requests urllib3
    echo ""
fi

# Run the demo
echo "🚀 Starting demo..."
echo ""
python3 demo_optim_api.py

echo ""
echo "=================================================="
echo "  Demo Complete!"
echo "=================================================="

# Made with Bob
