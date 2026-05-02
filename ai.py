import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def generate_ai_summary(portfolio, risk):
    if not api_key:
        return "OpenAI API key is missing. Please add OPENAI_API_KEY to your .env file."

    prompt = f"""
You are an AI portfolio assistant for a beginner-friendly wealth management app.

Analyze this portfolio:

Portfolio:
{portfolio}

Risk:
{risk}

Give a clear, short response with:
1. Portfolio summary
2. Main risk
3. News/sentiment observation
4. Suggested action
5. Educational disclaimer

Use simple language. Do not use complex financial jargon.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text


def generate_ai_recommendations(portfolio, risk):
    if not api_key:
        return []

    prompt = f"""
You are an AI portfolio recommendation engine for a beginner-friendly wealth management app.

Analyze this portfolio and create smart stock recommendations.

Portfolio:
{portfolio}

Risk:
{risk}

Return ONLY valid JSON.
No markdown.
No explanation outside JSON.

Return this exact structure:
[
  {{
    "symbol": "AAPL",
    "action": "BUY",
    "confidence": 78,
    "reason": "Short beginner-friendly explanation.",
    "priceTarget": "N/A"
  }}
]

Rules:
- action must be one of: BUY, SELL, HOLD
- confidence must be a number from 1 to 100
- reason should be simple and specific
- use risk, sector concentration, and sentiment if available
- do not give financial advice guarantees
- keep each reason under 25 words
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    text = response.output_text

    try:
        return json.loads(text)
    except Exception:
        return []