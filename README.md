# Personal Expense Tracker

A minimal, mobile-friendly personal finance companion built with Streamlit and Supabase. Track monthly expenses, set budgets, and view simple insights — all from your browser.

## Features

- **Home** — Current month spending, budget progress, category breakdown, recent expenses
- **Add Expense** — Quick entry with amount, category, date, payment method, and note
- **History** — Search, filter, edit, and delete expenses
- **Insights** — Category chart, daily trend, averages, and month-over-month comparison
- **More** — View categories/payment methods, set monthly budget, export CSV

## Tech Stack

- Streamlit (UI)
- Supabase PostgreSQL (database)
- Plotly + Pandas (charts and export)

## Local Setup

### 1. Clone and install

```bash
git clone https://github.com/sherlock-builds/personal-expense-tracker.git
cd personal-expense-tracker
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Set up Supabase

1. Create a free project at [supabase.com](https://supabase.com)
2. Open **SQL Editor** and run the contents of [`database/schema.sql`](database/schema.sql)
3. Go to **Project Settings → API** and copy:
   - Project URL
   - `service_role` key (keep this secret)

### 3. Configure secrets

Copy the example secrets file and fill in your values:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-service-role-key"
```

### 4. Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New app** and select your repository
4. Set **Main file path** to `app.py`
5. Under **Advanced settings → Secrets**, add:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-service-role-key"
```

6. Click **Deploy**

## Project Structure

```text
├── app.py                  # Entry point and navigation
├── pages/                  # App screens
├── database/               # Supabase connection and queries
├── utils/                  # Constants, formatting, calculations
├── assets/style.css        # Custom styling
└── .streamlit/config.toml  # Theme and layout
```

## Version

Version 1.0 — Core expense tracking, budgets, and basic insights.
