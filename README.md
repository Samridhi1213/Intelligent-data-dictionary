# Intelligent Data Dictionary Agent

An end‑to‑end data dictionary and analytics platform for extracting
metadata from relational databases, running data quality checks, and
producing AI‑powered documentation and conversational SQL support.

The system consists of a **Python backend** (FastAPI) that connects to
PostgreSQL, loads sample datasets, performs analysis, and calls the
Google Gemini model, and a **React/Vite frontend** that provides an
interactive dashboard and chat interface.

---

## 🔧 Prerequisites

Before you begin, install the following on your development machine:

- **Python 3.9 or later** (3.11+ recommended)
- **PostgreSQL** server (local or remote)
- **Node.js 18+** (for the frontend)
- A **Google Gemini API key** (obtainable via Google AI Studio)
- Optional: `virtualenv`/`venv` for isolating Python dependencies

---

##  Getting started

### 1. Create a Python virtual environment (recommended)

```powershell
cd "c:\Users\VICTUS\Documents\Intelligent data dictionaryy"
python -m venv .venv      # or use virtualenv/conda
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
```

### 2. Install backend dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file and edit it with your credentials and API key:

```powershell
cp .env.example .env      # Windows: copy .env.example .env
# then open .env in an editor and set:
#   DATABASE_URL=postgresql://user:pass@localhost/olist_db
#   GEMINI_API_KEY=your_key_here
```

Create the PostgreSQL database (e.g. `olist_db`) before running the
loader.

### 4. Load the sample datasets

Download the [Olist Kaggle dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
and unzip the CSVs into `backend/data/`.

From the project root run:

```bash
python -m backend.services.dataset_loader
```

This will parse the files, create tables and populate the database.

### 5. Starting the backend

Launch the API with:

```bash
python run_backend.py
```

By default the server listens on `http://localhost:8001`.

> 🔁 You can use the helper scripts at the repository root:
> - `find_working_model.py` – lists available Gemini models
> - `list_models.py` – alternative model inspection tool
> - `verify_gemini.py` – quick sanity check that your API key
>   works and returns a response.

### 6. Frontend setup

Open a second terminal, activate the same Python virtualenv (for
consistency if you call backend endpoints), then:

```bash
cd frontend
npm install
npm run dev
```

Point your browser to `http://localhost:5173` to view the dashboard.

---

## ✅ Key features

- **Automatic metadata extraction** using SQLAlchemy reflection
- **Data quality checks** (completeness, uniqueness, stats) over tables
- **Exportable reports** (JSON or pretty Markdown)
- **AI‑generated documentation** via Google Gemini
- **Conversational SQL** – ask natural‑language questions and receive
  SQL queries
- **Extensible connector framework** (see `backend/connectors/*.py`)

---

## 🛠️ Development notes

- Backend tests are not yet included; you can create them under
  `backend/tests/` and run with `pytest`.
- Updated database schema can be created by re‑running the loader or by
  editing the `dataset_loader` service.
- The frontend uses Vite+React and is intentionally lightweight; modify
  components in `frontend/src/components/`.

---

## 🧱 Tech Stack & Project Structure

### 🛠 Technology stack

| Layer      | Technologies / Libraries                          |
|------------|--------------------------------------------------|
| Backend    | Python 3.9+, FastAPI, SQLAlchemy, pg8000/psycopg2 |
| AI         | Google Gemini (via HTTP API)                     |
| Data store | PostgreSQL                                       |
| Frontend   | React, Vite, JSX, Tailwind (optional CSS)        |
| Dev tools  | npm, pip, virtualenv, Git                        |

External connectors implemented in `backend/connectors/` support
PostgreSQL, MSSQL, Snowflake, etc., via a simple inheritance model.

### 📂 Project layout

```
/                     # repo root
├─ backend/           # Python service
│  ├─ config.py       # environment/config utilities
│  ├─ main.py         # FastAPI entrypoint
│  ├─ requirements.txt
│  ├─ connectors/     # database adapter classes
│  │   ├─ base.py
│  │   ├─ mssql.py
│  │   ├─ postgres.py
│  │   └─ snowflake.py
│  └─ services/       # core business logic
│      ├─ ai_service.py
│      ├─ dataset_loader.py
│      ├─ export_service.py
│      ├─ metadata_service.py
│      └─ quality_service.py
├─ frontend/          # React/Vite application
│  ├─ src/
│  │   ├─ api.js      # http helpers
│  │   ├─ App.jsx
│  │   ├─ components/
│  │   │   ├─ ChatInterface.jsx
│  │   │   ├─ Dashboard.jsx
│  │   │   └─ TableExplorer.jsx
│  │   └─ main.jsx
│  ├─ index.html
│  ├─ package.json
│  └─ vite.config.js
├─ exports/           # generated reports/data dumps
│  └─ full_metadata.json
├─ data/              # sample CSVs (ignored by git)
├─ *.py               # utility scripts at root
│  ├─ find_working_model.py
│  ├─ list_models.py
│  ├─ run_backend.py
│  └─ verify_gemini.py
├─ README.md          # this document
└─ working_*.txt      # temporary output files
```

This structure keeps backend and frontend clearly separated and makes it
straightforward to extend with new connectors, tests, or UI components.

---

## 📄 License

This project is released under the MIT License. See `LICENSE` for
details.
