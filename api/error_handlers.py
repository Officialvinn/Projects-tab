# api/error_handlers.py
"""
Centralized JSON error responses for the MoMo API.
Keeps error format consistent across all endpoints.
"""
import json


def _send_error(handler, status_code, error, message):
    body = json.dumps({"error": error, "message": message}, indent=2).encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def error_400(handler, message="Bad request"):
    """Invalid or malformed input."""
    _send_error(handler, 400, "Bad Request", message)


def error_401(handler, message="Invalid or missing credentials. Use Basic Authentication."):
    """Authentication required or invalid credentials."""
    body = json.dumps(
        {"error": "Unauthorized", "message": message}, indent=2
    ).encode("utf-8")
    handler.send_response(401)
    handler.send_header("WWW-Authenticate", 'Basic realm="MoMo API"')
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def error_404(handler, message="Resource not found."):
    """Requested resource does not exist."""
    _send_error(handler, 404, "Not Found", message)


def error_500(handler, message="Internal server error."):
    """Something went wrong server-side."""
    _send_error(handler, 500, "Internal Server Error", message)