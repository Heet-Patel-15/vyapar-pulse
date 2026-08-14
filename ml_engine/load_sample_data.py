import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyapar_pulse.settings')
django.setup()

import pandas as pd
from core.models import Business, Product, TransactionRecord

def load_sample_data():
    # Create a business + product to attach transactions to
    business, _ = Business.objects.get_or_create(
        name="Test Kirana Store",
        defaults={"owner_email": "test@example.com"}
    )
    product, _ = Product.objects.get_or_create(
        business=business,
        product_name="General Sales",
        defaults={"category": "General"}
    )

    df = pd.read_csv("data/sample_transactions.csv", parse_dates=["transaction_date"])

    created_count = 0
    for _, row in df.iterrows():
        TransactionRecord.objects.create(
            business=business,
            product=product,
            transaction_type="sale",
            amount=row["amount"],
            quantity=1,
            transaction_date=row["transaction_date"].date(),
        )
        created_count += 1

    print(f"Loaded {created_count} transactions into MySQL.")

if __name__ == "__main__":
    load_sample_data()