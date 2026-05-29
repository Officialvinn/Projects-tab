from http.server import BaseHTTPRequestHandler
import json
import base64
import xml.etree.ElementTree as ET
import os
import re

# Authentication credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "momo2024"

# Load and parse the XML data
XML_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "modified_sms_v2.xml")

def load_transactions():
    """Parse the XML file and return a dictionary of transactions keyed by ID."""
    transactions = {}
    try:
        tree = ET.parse(XML_PATH)
        root = tree.getroot()
        for i, sms in enumerate(root.iter("sms"), start=1):
            tx_id = str(i)
            transactions[tx_id] = {
                "id"           : tx_id,
                "address"      : sms.attrib.get("address", ""),
                "date"         : sms.attrib.get("date", ""),
                "type"         : sms.attrib.get("type", ""),
                "body"         : sms.attrib.get("body", ""),
                "readable_date": sms.attrib.get("readable_date", ""),
                "contact_name" : sms.attrib.get("contact_name", ""),
            }
    except Exception as e:
        print(f"Warning: Could not load XML: {e}")
    return transactions


# Load transactions into memory at startup
TRANSACTIONS = load_transactions()


# Helper functions

def check_auth(handler):
    """Check Basic Auth credentials. Returns True if valid, False otherwise."""
    auth_header = handler.headers.get("Authorization", "")
    if not auth_header.startswith("Basic "):
        return False
    try:
        encoded = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username == VALID_USERNAME and password == VALID_PASSWORD
    except Exception:
        return False


def send_json(handler, status, data):
    """Send a JSON response."""
    body = json.dumps(data, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def send_unauthorized(handler):
    """Send a 401 Unauthorized response."""
    send_json(handler, 401, {
        "error": "Unauthorized",
        "message": "Invalid or missing credentials. Use Basic Authentication."
    })


def get_id_from_path(path):
    """Extract transaction ID from path like /transactions/5"""
    match = re.match(r"^/transactions/(\w+)$", path)
    return match.group(1) if match else None


def read_body(handler):
    """Read and parse JSON body from request."""
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    return json.loads(raw.decode("utf-8"))


# Request Handler

class MoMoRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{self.address_string()}] {format % args}")

    # GET

    def do_GET(self):
        if not check_auth(self):
            send_unauthorized(self)
            return

        # GET /transactions
        if self.path == "/transactions":
            send_json(self, 200, {
                "count": len(TRANSACTIONS),
                "transactions": list(TRANSACTIONS.values())
            })

        # GET /transactions/{id}
        elif get_id_from_path(self.path):
            tx_id = get_id_from_path(self.path)
            if tx_id in TRANSACTIONS:
                send_json(self, 200, TRANSACTIONS[tx_id])
            else:
                send_json(self, 404, {
                    "error": "Not Found",
                    "message": f"Transaction with id '{tx_id}' does not exist."
                })

        else:
            send_json(self, 404, {"error": "Not Found", "message": "Endpoint not found."})

    # POST

    def do_POST(self):
        if not check_auth(self):
            send_unauthorized(self)
            return

        if self.path == "/transactions":
            try:
                data = read_body(self)

                # Validate required fields
                required = ["address", "body"]
                missing = [f for f in required if f not in data]
                if missing:
                    send_json(self, 400, {
                        "error": "Bad Request",
                        "message": f"Missing required fields: {missing}"
                    })
                    return

                # Generate new ID
                new_id = str(max((int(k) for k in TRANSACTIONS.keys()), default=0) + 1)
                data["id"] = new_id
                TRANSACTIONS[new_id] = data

                send_json(self, 201, {
                    "message": "Transaction created successfully.",
                    "transaction": data
                })

            except json.JSONDecodeError:
                send_json(self, 400, {
                    "error": "Bad Request",
                    "message": "Request body must be valid JSON."
                })
        else:
            send_json(self, 404, {"error": "Not Found", "message": "Endpoint not found."})

    # PUT

    def do_PUT(self):
        if not check_auth(self):
            send_unauthorized(self)
            return

        tx_id = get_id_from_path(self.path)
        if tx_id:
            if tx_id not in TRANSACTIONS:
                send_json(self, 404, {
                    "error": "Not Found",
                    "message": f"Transaction with id '{tx_id}' does not exist."
                })
                return
            try:
                data = read_body(self)
                data["id"] = tx_id  # preserve the original ID
                TRANSACTIONS[tx_id].update(data)
                send_json(self, 200, {
                    "message": "Transaction updated successfully.",
                    "transaction": TRANSACTIONS[tx_id]
                })
            except json.JSONDecodeError:
                send_json(self, 400, {
                    "error": "Bad Request",
                    "message": "Request body must be valid JSON."
                })
        else:
            send_json(self, 404, {"error": "Not Found", "message": "Endpoint not found."})

    # DELETE

    def do_DELETE(self):
        if not check_auth(self):
            send_unauthorized(self)
            return

        tx_id = get_id_from_path(self.path)
        if tx_id:
            if tx_id not in TRANSACTIONS:
                send_json(self, 404, {
                    "error": "Not Found",
                    "message": f"Transaction with id '{tx_id}' does not exist."
                })
                return
            deleted = TRANSACTIONS.pop(tx_id)
            send_json(self, 200, {
                "message": "Transaction deleted successfully.",
                "deleted": deleted
            })
        else:
            send_json(self, 404, {"error": "Not Found", "message": "Endpoint not found."})