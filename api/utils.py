# api/utils.py
"""
Shared helpers: JSON response, body reading, path parsing, XML loading.
"""
import json
import os
import re
import xml.etree.ElementTree as ET


# --------------------------------------------------------------
# HTTP response helpers
# --------------------------------------------------------------

def send_json(handler, status, data):
    """Write a JSON response with the given status code."""
    body = json.dumps(data, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def read_body(handler):
    """Read and parse a JSON request body. Returns {} if empty."""
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    return json.loads(raw.decode("utf-8"))


# --------------------------------------------------------------
# Path parsing
# --------------------------------------------------------------

_ID_PATTERN = re.compile(r"^/transactions/(\w+)$")


def get_id_from_path(path):
    """Extract a transaction ID from a path like /transactions/5."""
    match = _ID_PATTERN.match(path)
    return match.group(1) if match else None


# --------------------------------------------------------------
# Data loading (XML -> dict)
# --------------------------------------------------------------

XML_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "raw", "modified_sms_v2.xml"
)


def load_transactions():
    """Parse the XML file and return a dict of transactions keyed by string id."""
    transactions = {}
    try:
        tree = ET.parse(XML_PATH)
        root = tree.getroot()
        for i, sms in enumerate(root.iter("sms"), start=1):
            tx_id = str(i)
            transactions[tx_id] = {
                "id":            tx_id,
                "address":       sms.attrib.get("address", ""),
                "date":          sms.attrib.get("date", ""),
                "type":          sms.attrib.get("type", ""),
                "body":          sms.attrib.get("body", ""),
                "readable_date": sms.attrib.get("readable_date", ""),
                "contact_name":  sms.attrib.get("contact_name", ""),
            }
    except Exception as e:
        print(f"Warning: Could not load XML: {e}")
    return transactions