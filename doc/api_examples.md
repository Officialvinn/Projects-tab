# MoMo REST API Documentation

Base URL: `http://localhost:8000`  
Authentication: Basic Auth (username: `admin`, password: `momo2024`)

---

## Authentication

All endpoints require Basic Authentication. Include credentials with every request.

**curl example:**
```bash
curl -u admin:momo2024 http://localhost:8000/transactions
```

**Invalid credentials response:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing credentials. Use Basic Authentication."
}
```

---

## Endpoints

### 1. GET /transactions
Returns a list of all transactions.

**Request:**
```bash
curl -u admin:momo2024 http://localhost:8000/transactions
```

**Response (200 OK):**
```json
{
  "count": 1691,
  "transactions": [
    {
      "id": "1",
      "address": "M-Money",
      "date": "1715351458724",
      "type": "1",
      "body": "You have received 2000 RWF from Jane Smith on your mobile money account.",
      "readable_date": "10 May 2024 4:30:58 PM",
      "contact_name": "(Unknown)"
    }
  ]
}
```

**Error Codes:**
| Code | Meaning |
|------|---------|
| 200 | Success |
| 401 | Unauthorized — invalid or missing credentials |

---

### 2. GET /transactions/{id}
Returns a single transaction by ID.

**Request:**
```bash
curl -u admin:momo2024 http://localhost:8000/transactions/1
```

**Response (200 OK):**
```json
{
  "id": "1",
  "address": "M-Money",
  "date": "1715351458724",
  "type": "1",
  "body": "You have received 2000 RWF from Jane Smith on your mobile money account.",
  "readable_date": "10 May 2024 4:30:58 PM",
  "contact_name": "(Unknown)"
}
```

**Error Codes:**
| Code | Meaning |
|------|---------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Transaction not found |

---

### 3. POST /transactions
Adds a new transaction record.

**Request:**
```bash
curl -u admin:momo2024 -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "address": "MTN",
    "body": "You have received 5000 RWF from Alice Mutoni. Your new balance: 5000 RWF.",
    "readable_date": "29 May 2026 10:00:00 AM",
    "contact_name": "Alice Mutoni"
  }'
```

**Required fields:** `address`, `body`

**Response (201 Created):**
```json
{
  "message": "Transaction created successfully.",
  "transaction": {
    "id": "1692",
    "address": "MTN",
    "body": "You have received 5000 RWF from Alice Mutoni. Your new balance: 5000 RWF.",
    "readable_date": "29 May 2026 10:00:00 AM",
    "contact_name": "Alice Mutoni"
  }
}
```

**Error Codes:**
| Code | Meaning |
|------|---------|
| 201 | Transaction created successfully |
| 400 | Bad Request — missing required fields or invalid JSON |
| 401 | Unauthorized |

---

### 4. PUT /transactions/{id}
Updates an existing transaction by ID.

**Request:**
```bash
curl -u admin:momo2024 -X PUT http://localhost:8000/transactions/1692 \
  -H "Content-Type: application/json" \
  -d '{
    "body": "Updated: You have received 10000 RWF from Alice Mutoni. Your new balance: 10000 RWF.",
    "contact_name": "Alice Mutoni"
  }'
```

**Response (200 OK):**
```json
{
  "message": "Transaction updated successfully.",
  "transaction": {
    "id": "1692",
    "address": "MTN",
    "body": "Updated: You have received 10000 RWF from Alice Mutoni. Your new balance: 10000 RWF.",
    "readable_date": "29 May 2026 10:00:00 AM",
    "contact_name": "Alice Mutoni"
  }
}
```

**Error Codes:**
| Code | Meaning |
|------|---------|
| 200 | Transaction updated successfully |
| 400 | Bad Request — invalid JSON |
| 401 | Unauthorized |
| 404 | Transaction not found |

---

### 5. DELETE /transactions/{id}
Deletes a transaction by ID.

**Request:**
```bash
curl -u admin:momo2024 -X DELETE http://localhost:8000/transactions/1692
```

**Response (200 OK):**
```json
{
  "message": "Transaction deleted successfully.",
  "deleted": {
    "id": "1692",
    "address": "MTN",
    "body": "Updated: You have received 10000 RWF from Alice Mutoni. Your new balance: 10000 RWF.",
    "readable_date": "29 May 2026 10:00:00 AM",
    "contact_name": "Alice Mutoni"
  }
}
```

**Error Codes:**
| Code | Meaning |
|------|---------|
| 200 | Transaction deleted successfully |
| 401 | Unauthorized |
| 404 | Transaction not found |

---

## Error Reference

| Code | Meaning |
|------|---------|
| 200 | OK — request successful |
| 201 | Created — new record added |
| 400 | Bad Request — invalid input |
| 401 | Unauthorized — invalid credentials |
| 404 | Not Found — endpoint or record does not exist |
