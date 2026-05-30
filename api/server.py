# api/server.py
"""
Start the MoMo REST API server.
Run from the repo root with:  python -m api.server
"""
from http.server import HTTPServer
from api.routes import MoMoRequestHandler


HOST = "localhost"
PORT = 8000


def run():
    server = HTTPServer((HOST, PORT), MoMoRequestHandler)
    print(f"MoMo API running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    run()
