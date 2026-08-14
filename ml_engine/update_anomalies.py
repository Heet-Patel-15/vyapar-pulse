import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyapar_pulse.settings')
django.setup()

from core.models import TransactionRecord
from sklearn.ensemble import IsolationForest
import pandas as pd

def update_anomaly_flags():
    # Pull all transactions from MySQL via Django ORM
    records = TransactionRecord.objects.all().values('id', 'amount')
    df = pd.DataFrame(list(records))

    if df.empty:
        print("No transactions found.")
        return

    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly_score'] = model.fit_predict(df[['amount']])
    df['is_anomaly'] = df['anomaly_score'] == -1

    # Write results back to MySQL, one row at a time
    updated_count = 0
    for _, row in df.iterrows():
        TransactionRecord.objects.filter(id=row['id']).update(is_anomaly=bool(row['is_anomaly']))
        updated_count += 1

    print(f"Updated {updated_count} records. Anomalies found: {df['is_anomaly'].sum()}")

if __name__ == "__main__":
    update_anomaly_flags()