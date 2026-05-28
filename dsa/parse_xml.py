# dsa/parse_xml.py
# Purpose: Parse modified_sms_v2.xml, extract SMS records,
# validate fields, extract transaction IDs from body text,
# and save the result as JSON.

import xml.etree.ElementTree as ET
import json
import os
import re  # re = regular expressions, used to find TxId inside body text


def extract_transaction_id(body):
    """
    Try to extract a Transaction ID from the SMS body text.
    MoMo SMS bodies contain IDs in different formats:

    Format 1: "TxId: 73214484437. Your payment..."
    Format 2: "*162*TxId:13913173274*S*Your payment..."
    Format 3: "Financial Transaction Id: 76662021700."
    Format 4: "*165*S*..." transfers — no TxId, use None

    We try each pattern in order and return the first match.
    If nothing found, return None.
    """
    # Pattern 1: TxId: followed by digits (with or without space)
    match = re.search(r'TxId[:\s*]+(\d+)', body)
    if match:
        return match.group(1)

    # Pattern 2: Financial Transaction Id: followed by digits
    match = re.search(r'Financial Transaction Id[:\s]+(\d+)', body)
    if match:
        return match.group(1)

    return None  # Some messages have no transaction ID


def parse_sms_xml(xml_path):
    """
    Read the XML file, extract all SMS records using attribute access,
    validate key fields, extract transaction IDs, and return a list of dicts.
    """

    if not os.path.exists(xml_path):
        print(f"ERROR: File not found: {xml_path}")
        return []

    tree = ET.parse(xml_path)
    root = tree.getroot()

    print(f"Root tag     : {root.tag}")
    print(f"Total in XML : {root.attrib.get('count', 'unknown')} records")

    records = []
    skipped = 0

    for sms in root.findall("sms"):

        # Use .get() because data is stored as ATTRIBUTES, not child tags
        address      = sms.get("address")
        date         = sms.get("date")
        body         = sms.get("body")
        sms_type     = sms.get("type")
        readable     = sms.get("readable_date")

        # Validation: skip records missing critical fields
        if not address or not body:
            print(f"Skipping record — address: {address}, body present: {bool(body)}")
            skipped += 1
            continue

        # Extract transaction ID from the body text
        tx_id = extract_transaction_id(body)

        record = {
            "address"         : address.strip(),
            "date"            : date.strip() if date else "unknown",
            "readable_date"   : readable.strip() if readable else "unknown",
            "type"            : sms_type.strip() if sms_type else "unknown",
            "transaction_id"  : tx_id,          # None if not found
            "body"            : body.strip(),
        }

        records.append(record)

    print(f"Parsed {len(records)} records. Skipped {skipped}.")
    return records


def save_as_json(records, output_path):
    """Save the list of SMS record dicts to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to: {output_path}")


if __name__ == "__main__":
    # XML file is in the project root, NOT inside dsa/
    XML_FILE  = "modified_sms_v2.xml"
    JSON_FILE = "dsa/sms_data.json"

    sms_records = parse_sms_xml(XML_FILE)

    if sms_records:
        save_as_json(sms_records, JSON_FILE)

        print("\n--- First record preview ---")
        first = sms_records[0]
        for key, value in first.items():
            # Truncate long body text for readability
            display = value if key != "body" else value[:80] + "..."
            print(f"  {key:16}: {display}")

        # Count how many records have a transaction ID vs not
        with_id    = sum(1 for r in sms_records if r["transaction_id"])
        without_id = sum(1 for r in sms_records if not r["transaction_id"])
        print(f"\nRecords WITH transaction ID   : {with_id}")
        print(f"Records WITHOUT transaction ID: {without_id}")
    else:
        print("No records found. Check your XML file.")
        