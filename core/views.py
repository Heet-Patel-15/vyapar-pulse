from django.shortcuts import render
from django.db.models import Avg
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import TransactionRecord, Advisory   

def dashboard(request):
    total_transactions = TransactionRecord.objects.count()
    anomaly_count = TransactionRecord.objects.filter(is_anomaly=True).count()
    avg_amount = TransactionRecord.objects.aggregate(avg=Avg('amount'))['avg'] or 0

    latest_advisory = Advisory.objects.first()
    advisory_text = latest_advisory.text if latest_advisory else "No advisory generated yet — run the pipeline."

    records = list(
        TransactionRecord.objects.order_by('transaction_date').values(
            'transaction_date', 'amount', 'is_anomaly'
        )
    )
    labels = [r['transaction_date'].strftime('%d %b') for r in records]
    values = [float(r['amount']) for r in records]
    anomaly_points = [
        {"x": r['transaction_date'].strftime('%d %b'), "y": float(r['amount'])}
        for r in records if r['is_anomaly']
    ]

    
    context = {
        "total_transactions": total_transactions,
        "anomaly_count": anomaly_count,
        "avg_amount": round(avg_amount, 2),
        "advisory_text": advisory_text,
        "chart_labels": json.dumps(labels, cls=DjangoJSONEncoder),
        "chart_values": json.dumps(values, cls=DjangoJSONEncoder),
        "chart_anomalies": json.dumps(anomaly_points, cls=DjangoJSONEncoder),
    }
    return render(request, "core/dashboard.html", context)