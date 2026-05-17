# MoMo SMS Data Processing System

> Enterprise-level fullstack application that processes Mobile Money (MoMo) SMS data in XML format, cleans and categorizes the transactions, stores them in a relational database, and visualizes insights through a web dashboard.

---

## Team

**Team Name:** [Team Alpha]

| Name | GitHub | Role |
|------|--------|------|
| Alvin | [@Officialvinn](https://github.com/Officialvinn) | Backend / ETL Lead |
| Stacey | [@mskanogo](https://github.com/mskanogo) | Database / API Lead |
| Jessica | [@BizimaCJ](https://github.com/BizimaCJ) | Frontend / Dashboard Lead |

---

## Project Description

This project ingests raw MoMo SMS messages exported as XML, runs them through an ETL pipeline (parse → clean → categorize → load), persists structured records in SQLite, and exposes the results through a static dashboard (with an optional FastAPI layer).

**Key features:**
- XML parsing with robust error handling and a dead-letter queue for unparseable records
- Normalization of amounts, dates, and phone numbers
- Rule-based categorization of transaction types (deposits, withdrawals, transfers, payments, airtime, etc.)
- Relational storage in SQLite
- Interactive dashboard with charts and tables for analysis

---

## System Architecture

The high-level architecture diagram is committed in this repository at **[`docs/architecture.png`](docs/architecture.png)**.

You can also view the live version here: **[🔗 Architecture Diagram](https://drive.google.com/file/d/1_Mnut36YyC2kpwxGVk6Nv6BLVdUu7LnY/view?ts=6a00ad0d)**

The system has four main layers: **Data Ingestion** (XML input) → **ETL Pipeline** (Python) → **Storage** (SQLite + JSON exports) → **Presentation** (static dashboard, optional API).

---

## Project Structure

```
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html                    # Dashboard entry
├── docs/
│   ├── architecture.png          # System architecture diagram
│   └── erd_diagram.png           # Database ERD diagram
├── web/                          # Frontend assets
├── data/
│   ├── raw/                      # Input XML (git-ignored)
│   ├── processed/                # Cleaned outputs
│   ├── db.sqlite3                # SQLite DB
│   └── logs/                     # ETL + dead-letter logs
├── etl/                          # Parse → clean → categorize → load
├── api/                          # Optional FastAPI layer
├── database/
│   └── database_setup.sql        # SQL schema and sample data
├── examples/
│   └── json_schemas.json         # JSON representations of all entities
├── scripts/                      # Bash runners
└── tests/                        # Unit tests
```

---

## Database Design

### Entity Relationship Diagram (ERD)

The full ERD is available at **[`docs/erd_diagram.png`](docs/erd_diagram.png)**.

The database is built around 8 core tables:

| Table | Description |
|-------|-------------|
| `TRANSACTIONS` | Core financial transaction records |
| `TRANSACTION_CATEGORIES` | Types of transactions (incoming, payment, withdrawal, etc.) |
| `TRANSACTION_PARTICIPANTS` | Junction table linking transactions to contacts (M:N) |
| `CONTACTS` | Senders and receivers involved in transactions |
| `SMS_MESSAGES` | Raw SMS data extracted from the MoMo XML file |
| `SMS_BACKUPS` | Metadata about the XML backup files |
| `SYSTEM_LOGS` | ETL pipeline processing logs per record |
| `USERS` | MoMo account holders who own the transaction data |

### Key Design Decisions
- **TRANSACTION_PARTICIPANTS** resolves the many-to-many relationship between transactions and contacts — one transaction can have multiple participants (sender, receiver, merchant) and one contact can appear in many transactions
- **SYSTEM_LOGS** links to both SMS_MESSAGES and TRANSACTIONS to track exactly where in the pipeline each record was processed or failed
- **Foreign key constraints** enforce referential integrity across all tables
- **Indexes** are added on frequently queried columns such as transaction_datetime, status, and category_id

### JSON Data Models

JSON schemas for all entities are available at **[`examples/json_schemas.json`](examples/json_schemas.json)**.

The file includes:
- Individual JSON objects for each table (Transactions, Categories, Contacts, Logs, SMS Messages, Users)
- One complete nested transaction object showing how all related data is structured in an API response

### SQL to JSON Mapping

| SQL Table | JSON Representation |
|-----------|-------------------|
| TRANSACTIONS | Root transaction object |
| TRANSACTION_CATEGORIES | Nested as `category` inside transaction |
| CONTACTS | Nested as `sender` and `receiver` inside transaction |
| SMS_MESSAGES | Nested as `sms` inside transaction |
| SYSTEM_LOGS | Nested as `log` inside transaction |
| USERS | Nested as `user` inside transaction |

---

## Getting Started

### Prerequisites
- Python 3.10+
- Git

### Setup
```bash
# 1. Clone the repo
git clone https://github.com/Officialvinn/Projects-tab.git
cd Projects-tab

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the env template
cp .env.example .env
```

### Run the ETL pipeline
```bash
bash scripts/run_etl.sh
```

### Serve the dashboard
```bash
bash scripts/serve_frontend.sh
# then open http://localhost:8000
```

---

## Project Management

*A screenshot of the board is also available at [`docs/scrum-board.png`]  
**Scrum Board (Trello):** [🔗 View our Trello Board](https://trello.com/b/JIxV6L3y/momo-dashboard?utm_source=eval-email&utm_medium=email&utm_campaign=board-invite)

We follow Agile practices with weekly sprints. Tasks are tracked across **To Do → In Progress → Done** columns.

---

## Testing

```bash
pytest tests/
```

---

## Project Timeline

| Week | Milestone |
|------|-----------|
| 1 | Team setup, architecture, Scrum board |
| 2 | Database design (ERD, SQL schema, JSON modeling) |
| 3 | ETL pipeline (parsing + cleaning + categorization) |
| 4 | Frontend dashboard |
| 5 | Integration, testing, polish |

---

## AI Usage

All AI interactions are documented in **[`AI_USAGE_LOG.md`](AI_USAGE_LOG.md)** in line with the course AI usage policy.