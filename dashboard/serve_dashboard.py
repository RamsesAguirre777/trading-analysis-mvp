#!/usr/bin/env python3
"""
Simple HTTP Server for Trading Dashboard
Serves the dashboard with proper CORS headers for local development
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urlparse


class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Custom logging format
        print(f"🌐 {self.address_string()} - {format % args}")


def main():
    PORT = 8080
    
    # Change to dashboard directory
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dashboard_dir)
    
    print(f"🚀 Starting Trading Dashboard Server...")
    print(f"📁 Serving from: {dashboard_dir}")
    print(f"🌐 Server URL: http://localhost:{PORT}")
    print(f"📊 Dashboard: http://localhost:{PORT}/index.html")
    print(f"📄 Data API: http://localhost:{PORT}/data/latest_analysis.json")
    print("✋ Press Ctrl+C to stop the server\n")
    
    # Create server
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        try:
            # Auto-open browser
            webbrowser.open(f'http://localhost:{PORT}/index.html')
            
            print("✅ Server started successfully!")
            httpd.serve_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Server error: {e}")


if __name__ == "__main__":
    main()