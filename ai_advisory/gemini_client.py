import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_advisory(anomaly_summary, forecast_summary):
    prompt = f"""
You are a business advisor for a small shop owner in India who has no technical background.

Anomaly data detected in their sales: {anomaly_summary}
Sales forecast for next 14 days: {forecast_summary}

Write a short, plain-language summary (3-4 sentences) explaining:
1. What happened in their business recently
2. What they should watch out for or do next

Avoid technical jargon. Write like you're talking to a shop owner, not a data scientist.
"""

    response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)
    return response.text

if __name__ == "__main__":
    # Quick test with dummy data
    test_anomaly = "Revenue dropped sharply on Feb 15 and spiked unusually on March 20"
    test_forecast = "Expected to average ₹5,200/day over the next two weeks"

    result = generate_advisory(test_anomaly, test_forecast)
    print(result)
    
