import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_summary(portfolio, risk):
    prompt = f"""
You are a helpful AI portfolio assistant.

Explain this portfolio to a beginner.

Portfolio:
{portfolio}

Risk:
{risk}

Return:
1. Simple portfolio summary
2. Main risk
3. Diversification advice
4. One rebalancing suggestion

Use simple words.
Add a short note that this is educational and not financial advice.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text