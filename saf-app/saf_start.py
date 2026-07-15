from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, mmap, os

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api':
            data = {"status": 0, "bpm": 0.0}
            if os.path.exists("/dev/shm/saf_shared_mem"):
                try:
                    with open("/dev/shm/saf_shared_mem", "rb") as f:
                        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                        data = {"status": int.from_bytes(mm[0:4], 'little'), 
                                "bpm": float(int.from_bytes(mm[4:8], 'little'))}
                except: pass
            self.send_response(200); self.send_header('Content-type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else: super().do_GET()

print("Server läuft auf http://localhost:8080"); HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
