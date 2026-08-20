# Vyapar Pulse — AI-Powered Business Health & Anomaly Intelligence Platform

Vyapar Pulse is a full-stack business intelligence platform built for small retailers who don't have access to enterprise-level analytics tools. It automatically detects unusual sales patterns, forecasts short-term revenue, and translates technical findings into plain-language business advice using generative AI.

## Problem Statement

Small and medium businesses (especially in India, where MSMEs contribute a significant share of GDP) largely operate without data analytics — no anomaly detection, no forecasting, no structured reporting. Vyapar Pulse closes that gap with an affordable, free-tier-friendly pipeline that a small business could realistically use.

## Features

- **Anomaly Detection** — Isolation Forest model flags unusual revenue days (sudden spikes or drops)
- **Revenue Forecasting** — ARIMA time-series model predicts next 14 days of revenue
- **AI Business Advisory** — Google Gemini API converts ML output into plain-language, non-technical advice for shop owners
- **Live Dashboard** — Custom Django front-end showing real-time KPIs, anomaly counts, and AI-generated advisories
- **Power BI Integration** — Live-connected BI dashboard with anomaly-highlighted visualizations

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django, Python |
| Database | MySQL |
| Machine Learning | scikit-learn (Isolation Forest), statsmodels (ARIMA) |
| Generative AI | Google Gemini API (`gemini-2.5-flash`) |
| BI/Reporting | Power BI Desktop |
| Frontend | Django Templates, Chart.js, custom CSS |
| Data Processing | Pandas, NumPy |

## Architecture
Data Ingestion (Pandas)
→ MySQL (via Django ORM)
→ ML Engine (Isolation Forest + ARIMA)
→ Anomaly flags written back to MySQL
→ AI Advisory (Gemini API) → saved to MySQL
→ Served via:
- Custom Django Dashboard (live KPIs + advisory)
- Power BI (connected live to MySQL)

## Project Structure
vyapar-pulse/
├── manage.py
├── requirements.txt
├── core/ # Django app — models, views, dashboard
│ ├── models.py # Business, Product, TransactionRecord, Advisory
│ ├── views.py
│ └── templates/core/dashboard.html
├── ml_engine/ # ML pipeline
│ ├── anomaly_detection.py
│ ├── forecasting.py
│ ├── update_anomalies.py
│ ├── load_kaggle_data.py
│ └── pipeline.py
├── ai_advisory/ # Gemini integration
│ └── gemini_client.py
├── data/ # Dataset (not committed — see below)
└── power_bi/
└── vyapar_pulse_dashboard.pbix

## Dataset

This project uses the **Online Retail II** dataset (UCI/Kaggle) — real transaction-level e-commerce data.

The raw CSV is not included in this repository (file size). To run this project:
1. Download the dataset from Kaggle: search "Online Retail II UCI"
2. Place it at `data/online_retail_II.csv`
3. Run the loader script (see Setup below)

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Heet-Patel-15/vyapar-pulse.git
cd vyapar-pulse
```

### 2. Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 3. Configure MySQL
Create a database:
```sql
CREATE DATABASE vyapar_pulse;
```
Update `vyapar_pulse/settings.py` with your MySQL credentials.

### 4. Set up environment variables
Create a `.env` file in the project root:
GEMINI_API_KEY=your_gemini_api_key_here

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Load data
```bash
python -m ml_engine.load_kaggle_data
```

### 7. Run the ML + AI pipeline
```bash
python -m ml_engine.update_anomalies
python -m ml_engine.pipeline
```

### 8. Start the server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/`

## Power BI Dashboard

1. Open `power_bi/vyapar_pulse_dashboard.pbix` in Power BI Desktop
2. Connect to your local MySQL instance using the built-in MySQL connector
3. Click Refresh to pull the latest data

Note: This project uses Power BI's free tier, so refresh is manual (scheduled auto-refresh requires Power BI Pro).


## Future Improvements

- Deploy to a cloud host (Render/Railway) with a cloud-hosted MySQL backend
- Add severity-based anomaly scoring instead of binary flags
- Multi-business support with user authentication

## Author

**Heet Kansagara**
[LinkedIn](https://linkedin.com/in/heet-kansagara) · [GitHub](https://github.com/Heet-Patel-15) · kansagaraheet15@gmail.com