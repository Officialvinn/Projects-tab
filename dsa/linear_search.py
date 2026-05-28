# dsa/linear_search.py
import json


def linear_search(records, target_tx_id):
    """
    Search the list of SMS records for a matching transaction ID.
    Returns the matching record or None.

    Time complexity: O(n) — checks every record until a match is found.
    """
    for i, record in enumerate(records):
        if record["transaction_id"] == target_tx_id:
            print(f"  Match found at index {i}")
            return record   # Transaction IDs are unique — stop at first match

    return None  # Not found


def load_records(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    records = load_records("dsa/sms_data.json")
    print(f"Total records loaded: {len(records)}")

    # Only test records that actually have a transaction ID
    records_with_id = [r for r in records if r["transaction_id"]]
    print(f"Records with transaction ID: {len(records_with_id)}")

    # Test 1: search for a transaction ID that exists (use the last one = worst case)
    target = records_with_id[-1]["transaction_id"]
    print(f"\nSearching for TxId: {target}")
    result = linear_search(records, target)
    if result:
        print(f"Found: {result['body'][:80]}...")

    # Test 2: search for a transaction ID that does NOT exist
    fake_id = "0000000000000"
    print(f"\nSearching for fake TxId: {fake_id}")
    result2 = linear_search(records, fake_id)
    if not result2:
        print("Not found (expected).")
        