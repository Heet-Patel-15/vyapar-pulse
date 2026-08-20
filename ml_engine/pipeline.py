def run_full_pipeline():
    records = TransactionRecord.objects.all().values('transaction_date', 'amount', 'is_anomaly')
    df = pd.DataFrame(list(records))
    df['amount'] = df['amount'].astype(float)

    daily = df.groupby('transaction_date')['amount'].sum().reset_index()
    daily = daily.sort_values('transaction_date')
    daily['amount'] = daily['amount'].astype(float)

    anomalies = df[df['is_anomaly'] == True]
    anomaly_summary = anomalies[['transaction_date', 'amount']].to_string(index=False)

    daily.set_index('transaction_date', inplace=True)
    model = ARIMA(daily['amount'], order=(2, 1, 2))
    fitted = model.fit()
    forecast = fitted.forecast(steps=14)
    forecast_summary = forecast.to_string()

    advisory_text = generate_advisory(anomaly_summary, forecast_summary)

    # Save to DB — update the single latest advisory row (id=1) or create it
    Advisory.objects.update_or_create(id=1, defaults={"text": advisory_text})

    return advisory_text