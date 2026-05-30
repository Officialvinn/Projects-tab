# api/validators.py
"""
Input validation for transaction requests.
Called by routes before any data is stored or updated.
"""
from api.schemas import REQUIRED_FIELDS


def validate_new_transaction(data):
    """
    Check that a new transaction payload has all required fields.
    Returns (True, None) if valid, or (False, error_message) otherwise.
    """
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object."

    missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
    if missing:
        return False, f"Missing required fields: {missing}"

    return True, None


def validate_update(data):
    """
    Check an update payload. PUT requests don't require all fields,
    only that at least one valid field is provided.
    """
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object."

    if not data:
        return False, "Request body cannot be empty."

    return True, None