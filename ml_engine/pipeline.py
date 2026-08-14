from ml_engine.anomaly_detection import detect_anomalies
from ml_engine.forecasting import forecast_sales
from ai_advisory.gemini_client import generate_advisory

def run_full_pipeline():
    df, anomalies = detect_anomalies()
    forecast = forecast_sales()

    anomaly_summary = anomalies[["transaction_date", "amount"]].to_string(index=False)
    forecast_summary = forecast.to_string()

    advisory = generate_advisory(anomaly_summary, forecast_summary)
    return advisory

if __name__ == "__main__":
    result = run_full_pipeline()
    print("=== BUSINESS ADVISORY ===")
    print(result)