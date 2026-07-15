from http.server import HTTPServer, SimpleHTTPRequestHandler
import mmap
class SAFHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/matrix':
            try:
                with open('saf_data/saf_shared_mem', 'rb') as f:
                    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                    data = mm.read(1024); mm.close()
                self.send_response(200); self.send_header('Content-type', 'application/octet-stream'); self.end_headers(); self.wfile.write(data)
            except: self.send_error(503)
        else: super().do_GET()
httpd = HTTPServer(('0.0.0.0', 8888), SAFHandler); httpd.serve_forever()
