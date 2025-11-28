#!/usr/bin/env python3.11

"""
Simple test script to verify MCP servers work independently
"""

import subprocess
import json
import time

def test_server(server_script, test_name):
    print(f"\n=== Testing {test_name} ===")
    try:
        # Start the server process
        process = subprocess.Popen(
            ['/opt/homebrew/bin/python3.11', server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Simple initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {
                        "listChanged": True
                    }
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send request
        request_str = json.dumps(init_request) + '\n'
        process.stdin.write(request_str)
        process.stdin.flush()
        
        # Wait a moment for response
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ {test_name} server started successfully")
            process.terminate()
            process.wait(timeout=5)
        else:
            print(f"❌ {test_name} server failed to start")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Error: {stderr}")
            
    except Exception as e:
        print(f"❌ Error testing {test_name}: {e}")
        if 'process' in locals():
            process.terminate()

def main():
    print("Testing MCP Servers...")
    
    # Test weather server
    test_server("weather_mcp_server.py", "Weather Server")
    
    # Test task server  
    test_server("tasklist_mcp_server.py", "Task Server")
    
    print("\n=== Test Summary ===")
    print("If both servers started successfully, you can run the full client with:")
    print("/opt/homebrew/bin/python3.11 mcp_client.py")

if __name__ == "__main__":
    main()