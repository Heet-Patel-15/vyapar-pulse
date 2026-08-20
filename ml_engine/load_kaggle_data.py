import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyapar_pulse.settings')
django.setup()

import pandas as pd
from core.models import Business, Product, TransactionRecord

def load_kaggle_data(csv_path="data/online_retail_ii.csv", limit=2000):
    df = pd.read_csv(csv_path, encoding="ISO-8859-1")

    # Basic cleaning
    df = df.dropna(subset=["Invoice", "InvoiceDate", "Price", "Quantity"])
    df = df[df["Quantity"] > 0]      # drop returns/cancellations
    df = df[df["Price"] > 0]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"])
    df = df.sort_values("InvoiceDate").head(limit)   # keep it manageable for free-tier DB

    business, _ = Business.objects.get_or_create(
        name="Online Retail Store",
        defaults={"owner_email": "demo@example.com"}
    )

    created_count = 0
    for _, row in df.iterrows():
        product, _ = Product.objects.get_or_create(
            business=business,
            product_name=str(row["Description"])[:100],
            defaults={"category": "General"}
        )
        TransactionRecord.objects.create(
            business=business,
            product=product,
            transaction_type="sale",
            amount=float(row["Price"]) * float(row["Quantity"]),
            quantity=int(row["Quantity"]),
            transaction_date=row["InvoiceDate"].date(),
        )
        created_count += 1

    print(f"Loaded {created_count} transactions from Kaggle dataset.")

if __name__ == "__main__":
    load_kaggle_data()