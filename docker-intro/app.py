from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Brian's AI Engineer API", "status": "alive"}
        self.wfile.write(json.dumps(response).encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Server running on port 8000...")
server.serve_forever()
