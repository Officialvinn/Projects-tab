# dsa/benchmark.py
# Purpose: Benchmark linear search vs dictionary lookup.
# Measures average time over many repetitions for a fair comparison.

import json
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dictionary_lookup import build_lookup_dict, dict_lookup


def load_records(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def linear_search_silent(records, target_tx_id):
    """
    Same logic as linear_search() but with NO print statements.
    We use this version during benchmarking so the 500 repetitions
    don't flood the terminal with 'Match found at index...' messages.
    Printing to terminal actually takes time and would skew the results.
    """
    for record in records:
        if record["transaction_id"] == target_tx_id:
            return record
    return None


def benchmark_linear(records, target, repetitions=500):
    """
    Run linear_search_silent() 500 times and return average time per search.
    """
    start = time.perf_counter()
    for _ in range(repetitions):
        linear_search_silent(records, target)
    end = time.perf_counter()

    return (end - start) / repetitions


def benchmark_dict(lookup_dict, target, repetitions=500):
    """
    Run dict_lookup() 500 times and return average time per lookup.
    The dictionary is already built before we start timing.
    We only time the lookup itself, not the build cost.
    """
    start = time.perf_counter()
    for _ in range(repetitions):
        dict_lookup(lookup_dict, target)
    end = time.perf_counter()

    return (end - start) / repetitions


if __name__ == "__main__":
    records = load_records("dsa/sms_data.json")
    print(f"Records loaded: {len(records)}")

    records_with_id = [r for r in records if r["transaction_id"]]

    # Build the dictionary index BEFORE timing starts
    print("Building dictionary index...")
    lookup = build_lookup_dict(records)

    # Use the LAST record's transaction ID — worst case for linear search
    # It must scan all 1691 records before finding the match at index 1690
    target = records_with_id[-1]["transaction_id"]
    print(f"Search target (worst case for linear): TxId {target}")
    print(f"Running 500 repetitions each — please wait...\n")

    linear_avg = benchmark_linear(records, target)
    dict_avg   = benchmark_dict(lookup, target)

    linear_ms = linear_avg * 1000
    dict_ms   = dict_avg   * 1000

    print("=" * 50)
    print(f"  Linear search average :  {linear_ms:.6f} ms")
    print(f"  Dictionary lookup avg  :  {dict_ms:.6f} ms")
    print("=" * 50)

    if dict_avg > 0:
        speedup = linear_avg / dict_avg
        print(f"  Dictionary is ~{speedup:.0f}x faster than linear search")

    print()
    print("Interpretation:")
    print(f"  Linear search scanned up to {len(records)} records per search.")
    print(f"  Dictionary jumped directly to the result every time.")
    print()
    print("Time complexity summary:")
    print("  Linear search  = O(n)  — time grows with number of records")
    print("  Dictionary     = O(1)  — time stays constant no matter the size")
    print()
    print("One-time dictionary build cost:")
    build_start = time.perf_counter()
    build_lookup_dict(records)
    build_end   = time.perf_counter()
    build_ms    = (build_end - build_start) * 1000
    print(f"  O(n) build took {build_ms:.4f} ms — paid once, then O(1) forever.")
    