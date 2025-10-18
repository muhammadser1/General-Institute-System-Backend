#!/usr/bin/env python3
"""
CORS Test Server
Run this to test CORS with multiple ports
"""

import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path

def run_server(port, filename):
    """Run a simple HTTP server on specified port"""
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"✅ Server running on http://localhost:{port}")
            print(f"   Serving: {filename}")
            print(f"   Press Ctrl+C to stop\n")
            
            # Open browser automatically
            url = f"http://localhost:{port}/{filename}"
            webbrowser.open(url)
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Server on port {port} stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use!")
            print(f"   Please close any application using port {port}")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/run_cors_test.py <port> <html_file>")
        print("\nExamples:")
        print("  python scripts/run_cors_test.py 3000 test_allowed_port.html")
        print("  python scripts/run_cors_test.py 4000 test_blocked_port.html")
        sys.exit(1)
    
    port = int(sys.argv[1])
    filename = sys.argv[2]
    
    # Check if file exists
    if not Path(filename).exists():
        print(f"❌ File not found: {filename}")
        sys.exit(1)
    
    print(f"🚀 Starting CORS test server...")
    print(f"   Port: {port}")
    print(f"   File: {filename}\n")
    
    run_server(port, filename)
