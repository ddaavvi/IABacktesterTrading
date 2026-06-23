"""
Quick server that serves the dashboard WITHOUT running the full backtester
"""
import http.server, socketserver, json, os, sys, time, urllib.parse

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PORT = 8000

_live_price_cache = {"prices": {}, "timestamp": 0}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_ROOT, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"loading": False}).encode('utf-8'))
            return
        
        if parsed_path.path == '/api/live-prices':
            global _live_price_cache
            now = time.time()
            if now - _live_price_cache["timestamp"] < 30 and _live_price_cache["prices"]:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(_live_price_cache["prices"]).encode('utf-8'))
                return
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(_live_price_cache["prices"]).encode('utf-8'))
            return
        
        super().do_GET()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Dashboard en http://localhost:{PORT}/web/")
        httpd.serve_forever()
