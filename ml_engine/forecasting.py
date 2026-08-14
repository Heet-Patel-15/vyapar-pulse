import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast_sales(csv_path="data/sample_transactions.csv", periods=14):
    df = pd.read_csv(csv_path, parse_dates=["transaction_date"])
    df.set_index("transaction_date", inplace=True)

    model = ARIMA(df["amount"], order=(2, 1, 2))
    fitted = model.fit()

    forecast = fitted.forecast(steps=periods)
    return forecast

if __name__ == "__main__":
    forecast = forecast_sales()
    print("Next 14-day forecast:")
    print(forecast)
    