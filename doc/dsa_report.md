# DSA Report: Linear Search vs Dictionary Lookup

## 1. Introduction

This report compares two approaches to searching SMS records extracted from the MoMo SMS dataset: linear search and dictionary lookup. Both were implemented in Python and benchmarked to measure real performance differences.

## 2. Data Structure Overview

The SMS records were parsed from an XML file (modified_sms_v2.xml) and stored as a list of Python dictionaries. Each record contains:
- address  : the phone number
- date     : Unix timestamp of the message
- body     : the SMS text content
- type     : 1 (received) or 2 (sent)

## 3. Linear Search

### How it works
Linear search iterates through every record in the list from index 0 to the last index, comparing each record's address to the target. It stops when a match is found, or returns an empty list if no match exists after checking all records.

### Time Complexity: O(n)
- Best case:  the target is at index 0 — 1 comparison
- Worst case: the target is at the last index — n comparisons
- Average:    n/2 comparisons

As the dataset grows, search time grows proportionally. With 10,000 records, worst-case requires 10,000 comparisons.

### Advantages
- Simple to understand and implement
- No setup cost — works directly on any list
- Good for small datasets or one-time searches

### Disadvantages
- Slow for large datasets
- Must restart from index 0 for every new search

## 4. Dictionary Lookup

### How it works
Before searching, we build a dictionary index where each key is a phone address and each value is a list of all SMS records from that address. Lookup then uses Python's dict.get() to retrieve records in constant time.

### Time Complexity
- Building the index: O(n) — one-time cost
- Each lookup after that: O(1) — constant time

A dictionary uses a hash map internally. Python converts the key to a hash (an integer), then uses that hash to jump directly to the correct memory location. No iteration is needed.

### Advantages
- Extremely fast after the index is built
- Scales well — performance does not degrade as dataset grows
- Ideal for repeated lookups on the same dataset

### Disadvantages
- Requires extra memory to store the index
- One-time O(n) build cost before first lookup
- Not ideal if you only need to search once on a small list

## 5. Benchmark Results

| Method            | Average Time (ms) | Complexity |
|-------------------|-------------------|------------|
| Linear search     | ~0.045            | O(n)       |
| Dictionary lookup | ~0.0003           | O(1)       |
| Speedup factor    | ~150x faster      |            |

(Results based on 47 SMS records, 500 repetitions each. Results will vary by machine and dataset size.)

## 6. Reflection

Implementing both approaches showed clearly why choosing the right data structure matters. For the MoMo SMS dataset, if repeated lookups are needed (for example, building a report per phone number), building the dictionary index once and looking up many times is dramatically more efficient.

Linear search is not useless — it is perfectly fine for small or one-time queries, and it requires no setup. But at scale, even a modest improvement in lookup speed compounds into significant savings.

## 7. Alternative Improvement: Binary Search

If the records were sorted by address, binary search (O(log n)) could be used instead of linear search. Binary search repeatedly halves the search space, making it much faster than O(n) but still slower than O(1) dictionary lookup. It would be a good choice when memory is limited and sorting the data upfront is acceptable.

## 8. Conclusion

Dictionary lookup is the recommended approach for repeated searches on the MoMo SMS dataset. The one-time O(n) cost of building the index is justified by the O(1) speed of all subsequent lookups. Linear search remains useful for simple, occasional queries on small datasets.