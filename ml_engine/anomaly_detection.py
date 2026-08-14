import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(csv_path="data/sample_transactions.csv"):
    df = pd.read_csv(csv_path, parse_dates=["transaction_date"])

    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly_score"] = model.fit_predict(df[["amount"]])

    # -1 means anomaly, 1 means normal
    df["is_anomaly"] = df["anomaly_score"] == -1

    anomalies = df[df["is_anomaly"]]
    return df, anomalies

if __name__ == "__main__":
    df, anomalies = detect_anomalies()
    print(f"Total records: {len(df)}")
    print(f"Anomalies detected: {len(anomalies)}")
    print(anomalies[["transaction_date", "amount"]])