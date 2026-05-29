from http.server import HTTPServer
from api.routes import MoMoRequestHandler
import json
import sys
import os

# Add parent directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes import MoMoRequestHandler

HOST = "localhost"
PORT = 8000


def run():
    server = HTTPServer((HOST, PORT), MoMoRequestHandler)
    print(f" MoMo API running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n Server stopped.")
        server.server_close()


if __name__ == "__main__":
    run()