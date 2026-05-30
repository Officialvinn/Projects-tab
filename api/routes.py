# api/routes.py
"""
HTTP routing for the MoMo API.
Auth, validation, and error handling are imported from sibling modules.
"""
from http.server import BaseHTTPRequestHandler
import json

from api.auth import is_authenticated
from api.error_handlers import error_400, error_401, error_404
from api.utils import send_json, read_body, get_id_from_path, load_transactions
from api.validators import validate_new_transaction, validate_update


# Load data once at startup
TRANSACTIONS = load_transactions()


class MoMoRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

    # ---------- GET ----------
    def do_GET(self):
        if not is_authenticated(self):
            return error_401(self)

        if self.path == "/transactions":
            return send_json(self, 200, {
                "count": len(TRANSACTIONS),
                "transactions": list(TRANSACTIONS.values()),
            })

        tx_id = get_id_from_path(self.path)
        if tx_id:
            if tx_id in TRANSACTIONS:
                return send_json(self, 200, TRANSACTIONS[tx_id])
            return error_404(self, f"Transaction with id '{tx_id}' does not exist.")

        return error_404(self, "Endpoint not found.")

    # ---------- POST ----------
    def do_POST(self):
        if not is_authenticated(self):
            return error_401(self)

        if self.path != "/transactions":
            return error_404(self, "Endpoint not found.")

        try:
            data = read_body(self)
        except json.JSONDecodeError:
            return error_400(self, "Request body must be valid JSON.")

        ok, msg = validate_new_transaction(data)
        if not ok:
            return error_400(self, msg)

        new_id = str(max((int(k) for k in TRANSACTIONS.keys()), default=0) + 1)
        data["id"] = new_id
        TRANSACTIONS[new_id] = data
        send_json(self, 201, {
            "message": "Transaction created successfully.",
            "transaction": data,
        })

    # ---------- PUT ----------
    def do_PUT(self):
        if not is_authenticated(self):
            return error_401(self)

        tx_id = get_id_from_path(self.path)
        if not tx_id:
            return error_404(self, "Endpoint not found.")

        if tx_id not in TRANSACTIONS:
            return error_404(self, f"Transaction with id '{tx_id}' does not exist.")

        try:
            data = read_body(self)
        except json.JSONDecodeError:
            return error_400(self, "Request body must be valid JSON.")

        ok, msg = validate_update(data)
        if not ok:
            return error_400(self, msg)

        data["id"] = tx_id  # preserve the original ID
        TRANSACTIONS[tx_id].update(data)
        send_json(self, 200, {
            "message": "Transaction updated successfully.",
            "transaction": TRANSACTIONS[tx_id],
        })

    # ---------- DELETE ----------
    def do_DELETE(self):
        if not is_authenticated(self):
            return error_401(self)

        tx_id = get_id_from_path(self.path)
        if not tx_id:
            return error_404(self, "Endpoint not found.")

        if tx_id not in TRANSACTIONS:
            return error_404(self, f"Transaction with id '{tx_id}' does not exist.")

        deleted = TRANSACTIONS.pop(tx_id)
        send_json(self, 200, {
            "message": "Transaction deleted successfully.",
            "deleted": deleted,
        })
