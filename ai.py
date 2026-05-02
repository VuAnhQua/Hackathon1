import os
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