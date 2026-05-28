# dsa/dictionary_lookup.py
import json


def build_lookup_dict(records):
    """
    Build a dictionary indexed by transaction_id for O(1) lookup.
    Key   = transaction_id (string)
    Value = the SMS record dict

    Records without a transaction_id are skipped — they have no unique key.
    """
    lookup = {}

    for record in records:
        tx_id = record["transaction_id"]
        if tx_id:  # Only index records that have a transaction ID
            lookup[tx_id] = record

    print(f"Dictionary built with {len(lookup)} indexed transaction IDs.")
    return lookup


def dict_lookup(lookup_dict, target_tx_id):
    """
    Look up a record by transaction ID in O(1) time.
    Returns the record dict, or None if not found.
    """
    return lookup_dict.get(target_tx_id)


def load_records(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    records = load_records("dsa/sms_data.json")
    lookup  = build_lookup_dict(records)

    # Test 1: look up a transaction ID that exists
    records_with_id = [r for r in records if r["transaction_id"]]
    target = records_with_id[-1]["transaction_id"]
    print(f"\nLooking up TxId: {target}")
    result = dict_lookup(lookup, target)
    if result:
        print(f"Found: {result['body'][:80]}...")

    # Test 2: look up a transaction ID that does NOT exist
    fake_id = "0000000000000"
    print(f"\nLooking up fake TxId: {fake_id}")
    result2 = dict_lookup(lookup, fake_id)
    if not result2:
        print("Not found (expected).")
        