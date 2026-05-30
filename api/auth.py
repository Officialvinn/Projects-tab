# api/auth.py
"""
Basic Authentication for the MoMo API.

NOTE: Basic Auth encodes credentials in base64, which is NOT encryption.
Over plain HTTP, credentials are recoverable by any network observer.
See docs/security_report.md for limitations and stronger alternatives.
"""
import base64


# Valid credentials. In production these would be hashed and stored
# in a database, never written in source code.
VALID_USERS = {
    "admin": "momo2024",
}


def _decode_basic_auth(header_value):
    """
    Decode a 'Basic <base64>' header value into (username, password).
    Returns (None, None) if missing or malformed.
    """
    if not header_value or not header_value.startswith("Basic "):
        return None, None

    encoded = header_value[len("Basic "):].strip()
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
    except Exception:
        return None, None

    if ":" not in decoded:
        return None, None

    username, password = decoded.split(":", 1)
    return username, password


def is_authenticated(handler):
    """
    Returns True if the request carries valid Basic Auth credentials.
    `handler` is a BaseHTTPRequestHandler instance.
    """
    auth_header = handler.headers.get("Authorization", "")
    username, password = _decode_basic_auth(auth_header)

    if username is None:
        return False

    expected_password = VALID_USERS.get(username)
    return expected_password is not None and password == expected_password