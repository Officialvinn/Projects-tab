# DSA Report: Linear Search vs Dictionary Lookup
## MoMo SMS Data — Student 1

---

## 1. Introduction

This report documents the implementation and comparison of two search approaches applied to a real MoMo SMS dataset: linear search and dictionary lookup. Both were implemented in Python, tested against 1,691 SMS records parsed from `modified_sms_v2.xml`, and benchmarked to measure real performance differences.

The goal was to understand how data structure choice affects search speed, and to reflect on which approach is more suitable for this dataset.

---

## 2. Dataset Overview

The SMS records were parsed from `modified_sms_v2.xml` — a backup of MTN MoMo SMS messages — using Python's built-in `xml.etree.ElementTree` library.

Key findings during parsing:
- Total SMS records in file  : 1,693
- Successfully parsed        : 1,691
- Skipped (missing fields)   : 2

Each parsed record was stored as a Python dictionary with these fields:

| Field            | Description                          | Example                        |
|------------------|--------------------------------------|--------------------------------|
| address          | SMS sender name                      | M-Money                        |
| date             | Unix timestamp (milliseconds)        | 1715351458724                  |
| readable_date    | Human-readable date and time         | 10 May 2024 4:30:58 PM         |
| type             | Message type (1 = received)          | 1                              |
| transaction_id   | Extracted transaction ID from body   | 76662021700                    |
| body             | Full SMS text content                | You have received 2000 RWF...  |

### Important discovery about the address field

Every single SMS record has `address="M-Money"` — the sender is always MTN MoMo, not individual phone numbers. This made the address field useless as a unique search key.

Instead, transaction IDs were extracted from the body text using Python's `re` (regular expressions) module. Two body formats were handled:

- Format 1: `TxId: 73214484437. Your payment...`
- Format 2: `Financial Transaction Id: 76662021700.`

Out of 1,691 records:
- Records WITH a transaction ID  : 823
- Records WITHOUT a transaction ID: 868

Records without a transaction ID are transfer-type messages (e.g. `*165*S*` format) that contain no TxId in their body text.

---

## 3. Linear Search

### Implementation

Linear search is implemented in `dsa/linear_search.py`. It loops through every record in the list from index 0 to the last index,comparing each record's `transaction_id` field to the target value. It returns the matching record immediately when found, or `None` if no match exists after checking all records.

### Time Complexity: O(n)

- Best case  : target is at index 0 — 1 comparison needed
- Worst case : target is at the last index — n comparisons needed
- Average    : n/2 comparisons

In our benchmark we deliberately tested the worst case — the target transaction ID was at index 1,690 out of 1,691 records. Linear search had to compare every single record before finding it.

### Advantages
- Simple to understand and implement
- No setup cost — works directly on any list
- Suitable for small datasets or one-time searches

### Disadvantages
- Slow for large datasets
- Performance degrades as the dataset grows
- Must restart from index 0 for every new search query

---

## 4. Dictionary Lookup

### Implementation

Dictionary lookup is implemented in `dsa/dictionary_lookup.py`. Before any searching can happen, a dictionary index is built once by looping through all records and storing each one under its transaction ID as the key. After that, any lookup is done with a single `dict.get()` call.

### Time Complexity

- Building the index : O(n) — one-time cost paid before first lookup
- Each lookup        : O(1) — constant time regardless of dataset size

Python dictionaries use a hash map internally. When you call `dict.get(key)`, Python converts the key into a number called a hash, then uses that number to jump directly to the correct memory location. No iteration over records is needed at all.

### Advantages
- Extremely fast after the index is built
- Performance does not degrade as the dataset grows
- Ideal when the same dataset is searched many times

### Disadvantages
- Requires extra memory to store the index structure
- One-time O(n) build cost must happen before the first lookup
- Only indexes records that have a transaction ID (823 out of 1,691)
- Not worth the setup cost if you only need to search once

---

## 5. Benchmark Results

Benchmarks were run on 1,691 records with 500 repetitions each. The search target was TxId `37832903831` located at index 1,690 — deliberately chosen as the worst case for linear search.

| Method                  | Average time per search | Complexity |
|-------------------------|-------------------------|------------|
| Linear search           | 0.273603 ms             | O(n)       |
| Dictionary lookup       | 0.000080 ms             | O(1)       |
| One-time build cost     | 0.1779 ms               | O(n)       |
| Speedup factor          | ~3,424x faster          |            |

### How to read these results

Linear search took 0.273603 ms on average because it scanned up to 1,691 records every single time. Dictionary lookup took 0.000080 ms because it jumped directly to the result using the hash of the key.

The one-time build cost of 0.1779 ms is paid only once when the program starts. After that, every subsequent lookup costs only 0.000080 ms. If you perform even 2 lookups, the dictionary has already recovered its build cost many times over.

---

## 6. Reflection

Implementing both approaches on real MoMo SMS data revealed several practical lessons beyond textbook theory.

First, data structure matters more than algorithm cleverness. The dictionary lookup is not a complex algorithm — it is simply choosing the right data structure (a hash map) for the problem. That single choice made lookups 3,424 times faster than linear search.

Second, real data is messy. The original plan was to search by phone address, but the dataset had `address="M-Money"` for every record — meaning the address field was not useful as a unique identifier. This required adapting the approach mid-way: extracting transaction IDs from the SMS body text using regular expressions. This kind of adaptation is normal in real software development.

Third, not every record is searchable. Only 823 of 1,691 records contained a transaction ID. The remaining 868 were transfer-type messages in a different format. A production system would need to handle those separately, perhaps with a different parsing strategy.

---

## 7. Alternative: Binary Search

If the records were sorted by transaction ID, binary search (O(log n)) could replace linear search. Binary search works by repeatedly halving the search space — checking the middle record, then searching only the left or right half depending on whether the target is smaller or larger.

For 1,691 records, binary search would need at most 11 comparisons (log₂ 1691 ≈ 11) compared to linear search's worst case of 1,691 comparisons. However, it still cannot match dictionary lookup's O(1) constant time. Binary search would be a good middle ground when memory is limited and sorting the data upfront is acceptable.

---

## 8. Conclusion

Dictionary lookup is the strongly recommended approach for repeated searches on the MoMo SMS dataset. The one-time O(n) build cost of 0.1779 ms is negligible compared to the 3,424x speed improvement on every subsequent lookup.

Linear search remains useful for simple, one-time queries on small datasets where setup cost is not justified. For a dataset of 1,691 records that will be searched many times — such as generating per-transaction reports or fraud detection — the dictionary approach is clearly superior.

---