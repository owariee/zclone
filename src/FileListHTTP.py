import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

#FileListHTTPRequestHandler
class FileListHTTP(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(404, "Directory not found")
            return None

        entries.sort(key=lambda x: x.lower())
        files = []
        for name in entries:
            file_path = os.path.join(path, name)
            file_stat = os.stat(file_path)
            files.append(f'<li><a href="{name}">{name}</a></li>')
        return '\n'.join(files)

    def do_GET(self):
        # Serve the directory listing if it's a directory
        if self.path.endswith('/'):
            directory_listing = self.list_directory(self.translate_path(self.path))
            if directory_listing:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f"""
                <!DOCTYPE html>
                <html>
                <head><title>Directory listing</title></head>
                <body>
                <h1>Directory listing</h1>
                <ul>
                {directory_listing}
                </ul>
                </body>
                </html>
                """.encode())
                return
        # Serve the file normally if it's not a directory
        super().do_GET()