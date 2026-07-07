# SchemaSay

SchemaSay is a natural language analytics platform that enables non-technical users to query databases using plain English. The platform retrieves database schemas, constructs context-aware LLM prompts, generates secure SQL statements, executes them on the target database, and returns dynamic visualizations alongside business insights.

## Core Architecture & Hardening Features

The system is structured as an enterprise-grade analytics pipeline:

1. **User Input:** Natural language question is submitted.
2. **Introspection:** Active database schema is retrieved and formatted as LLM context.
3. **Prompt Generation:** Prompt containing database structure, constraints, and user question is built.
4. **AI Generation:** LLM generates a read-only SQL query.
5. **SQL Sandbox Validation:** Query is scanned using `sqlglot` AST parsing to block:
   * Destructive statements (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`).
   * Stacked commands (semicolon query injections).
   * UNION exfiltration routes.
   * CTE write bypasses (`WITH ... INSERT/DELETE`) and `SELECT INTO` nodes.
   * Blind SQL injection timing vectors (`pg_sleep()`, `sleep()`, `WAITFOR`).
6. **Execution Engine:** Query runs asynchronously against the target database via:
   * Thread-safe execution pools (`run_in_threadpool`).
   * Strict 30-second timeouts enforced across dialects (PostgreSQL, MSSQL, MySQL, and C-level SQLite progress handlers).
   * Resource-capping registries using LRU connection pool eviction (strictly limited to 50 active engines).
   * Secured error masking (suppresses driver details, returning formatted generic feedback).
   * Request rate limiting (30 requests/minute per host).
7. **Visualization:** Evaluates DataFrame types to configure Plotly charts:
   * Handles nulls, mixed formats, non-ISO dates (`DD-MM-YYYY`, `MM/DD/YYYY`), Unix timestamps, and timezone-aware datetimes.
   * Sanitizes all columns, axes, and titles to protect against DOM XSS vectors.
   * Aggregates duplicate date series and sorts chronological inputs.
   * Enforces 5,000-row sampling limits and 15-category color thresholds to prevent browser locks.
8. **AI Insights:** Second LLM stage interprets results and generates a natural language business summary.

## Technology Stack

- **Backend:** FastAPI, Python, SQLAlchemy ORM, Alembic migrations, Pandas, Numpy, SQLGlot
- **Frontend:** Streamlit, Plotly Express
- **AI Engine:** OpenAI API (GPT-4) / Gemini API (GPT compatibility layer)
- **Database:** PostgreSQL (platform metadata)
- **Security:** JWT Auth with tokens rotation, bcrypt hashing, Fernet symmetric credential encryption, AST-based `sqlglot` read-only sandboxes, rate-limit gates, connection pool evictions, and DOM XSS sanitizers

## Repository Structure

```
schemasay/
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── api/              # Route handlers
│   │   ├── core/             # Business logic (auth, execution, schema introspection, AI)
│   │   ├── models/           # ORM models (SQLAlchemy)
│   │   ├── schemas/          # Pydantic schemas
│   │   └── utils/            # General helpers
│   └── requirements.txt
└── frontend/                 # Streamlit frontend application
    ├── app.py                # UI entry point
    ├── api_client.py         # HTTP client wrapper
    └── requirements.txt
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- OpenAI API Key

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/schemasay.git
   cd schemasay
   ```

2. Set up environment variables:
   Copy `.env.example` to `.env` and fill in your configuration keys:
   ```bash
   cp .env.example .env
   ```

3. Start the PostgreSQL database:
   ```bash
   docker compose up -d
   ```

4. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

5. Set up the frontend:
   Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd frontend
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

### Database Migrations

Initialize and update your PostgreSQL database schemas using Alembic:
```bash
cd backend
# Apply migrations to local PostgreSQL database
venv\Scripts\alembic upgrade head
```

### Running the Test Suite

Validate authentication security, token rotation, brute-force lockouts, symmetric database credential encryption, and spreadsheet file ingestion pipelines using the automated test suite:
```bash
# Execute isolated, in-memory SQLite integration test cases
venv\Scripts\pytest backend/tests/
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
