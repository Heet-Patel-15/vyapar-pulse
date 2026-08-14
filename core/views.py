from django.shortcuts import render
from .models import TransactionRecord

def dashboard(request):
    total_transactions = TransactionRecord.objects.count()
    anomaly_count = TransactionRecord.objects.filter(is_anomaly=True).count()
    context = {
        "total_transactions": total_transactions,
        "anomaly_count": anomaly_count,
        "advisory_text": "Run the pipeline to generate live advisory text here.",
    }
    return render(request, "core/dashboard.html", context)