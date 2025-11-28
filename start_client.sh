#!/bin/bash

# Enhanced Multi-Server MCP Startup Script

echo "Starting Enhanced Multi-Server MCP Client..."

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install mcp>=1.0.0
pip install langchain-mcp-adapters
pip install langgraph
pip install langchain-core
pip install langchain-google-genai
pip install python-dotenv
pip install requests
pip install fastmcp
pip install typing-extensions

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please copy .env.example to .env and add your API keys:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your actual API keys"
    echo ""
fi

# Run the enhanced MCP client
echo "Starting the enhanced MCP client..."
python mcp_client.py