# api/schemas.py
"""
Shape definitions for transaction records.
Used by validators to enforce consistent structure.
"""

# Fields a client MUST provide when creating a transaction
REQUIRED_FIELDS = ["address", "body"]

# Fields the API recognizes (anything outside this set is ignored)
ALLOWED_FIELDS = [
    "id",
    "address",
    "date",
    "type",
    "body",
    "readable_date",
    "contact_name",
]
