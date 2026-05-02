import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


POSITIVE_WORDS = [
    "growth", "beat", "beats", "strong", "surge", "rally",
    "gain", "gains", "positive", "upgrade", "bullish",
    "record", "profit", "profits", "outperform"
]

NEGATIVE_WORDS = [
    "fall", "falls", "drop", "drops", "weak", "loss",
    "losses", "negative", "downgrade", "bearish", "risk",
    "lawsuit", "decline", "miss", "cuts", "layoffs"
]


def get_news_sentiment(ticker: str):
    if not NEWS_API_KEY:
        return {
            "ticker": ticker,
            "sentiment": "Unavailable",
            "summary": "NewsAPI key is missing.",
            "articles": []
        }

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": ticker,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "ticker": ticker,
            "sentiment": "Unavailable",
            "summary": "Could not fetch news articles.",
            "articles": []
        }

    data = response.json()
    articles = data.get("articles", [])

    score = 0
    clean_articles = []

    for article in articles:
        title = article.get("title") or ""
        description = article.get("description") or ""
        text = f"{title} {description}".lower()

        for word in POSITIVE_WORDS:
            if word in text:
                score += 1

        for word in NEGATIVE_WORDS:
            if word in text:
                score -= 1

        clean_articles.append({
            "title": article.get("title"),
            "source": article.get("source", {}).get("name"),
            "url": article.get("url"),
            "publishedAt": article.get("publishedAt")
        })

    if score > 1:
        sentiment = "Positive"
    elif score < -1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "ticker": ticker.upper(),
        "sentiment": sentiment,
        "sentiment_score": score,
        "summary": f"Recent news sentiment for {ticker.upper()} appears {sentiment.lower()}.",
        "articles": clean_articles
    }