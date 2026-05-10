# MoMo SMS Data Processing System

> Enterprise-level fullstack application that processes Mobile Money (MoMo) SMS data in XML format, cleans and categorizes the transactions, stores them in a relational database, and visualizes insights through a web dashboard.

---

## Team

**Team Name:** [Your Team Name]

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
│   └── architecture.png          # System architecture diagram
├── web/                          # Frontend assets
├── data/
│   ├── raw/                      # Input XML (git-ignored)
│   ├── processed/                # Cleaned outputs
│   ├── db.sqlite3                # SQLite DB
│   └── logs/                     # ETL + dead-letter logs
├── etl/                          # Parse → clean → categorize → load
├── api/                          # Optional FastAPI layer
├── scripts/                      # Bash runners
└── tests/                        # Unit tests
```

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
| 2 | ETL pipeline (parsing + cleaning) |
| 3 | Database schema + categorization |
| 4 | Frontend dashboard |
| 5 | Integration, testing, polish |

---
