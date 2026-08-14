import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range(start="2025-01-01", periods=180, freq="D")

# Normal sales with some randomness
sales = np.random.normal(loc=5000, scale=800, size=180)

# Inject a few anomalies (sudden drops/spikes) to test detection later
sales[45] = 1200   # sudden drop
sales[90] = 12000  # sudden spike
sales[130] = 900    # sudden drop

df = pd.DataFrame({
    "transaction_date": dates,
    "amount": sales.round(2)
})

df.to_csv("data/sample_transactions.csv", index=False)
print("Sample data created:", df.shape)