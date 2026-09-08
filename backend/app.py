from http.server import BaseHTTPRequestHandler, HTTPServer
import json

def json_response(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/health":
            return json_response(self, 200, {
                "status": "ok",
                "service": "health-rehab-system",
                "sprint": 1
            })
        return json_response(self, 404, {"error": "not_found"})

if __name__ == "__main__":
    print("API running at http://localhost:8000")
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
