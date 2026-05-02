from fastapi import FastAPI

from models import PortfolioRequest
from market import get_stock_data
from risk import calculate_risk
from ai import generate_ai_summary
from sentiment import get_news_sentiment

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.post("/analyze")
def analyze_portfolio(request: PortfolioRequest):
    portfolio_results = []

    for item in request.portfolio:
        stock_data = get_stock_data(item.ticker, item.amount)

        sentiment_data = get_news_sentiment(item.ticker)

        stock_data["sentiment"] = sentiment_data

        portfolio_results.append(stock_data)

    risk_result = calculate_risk(portfolio_results)

    try:
        ai_summary = generate_ai_summary(portfolio_results, risk_result)
    except Exception:
        ai_summary = "AI temporarily unavailable."

    return {
        "portfolio": portfolio_results,
        "risk": risk_result,
        "ai_summary": ai_summary
    }

@app.get("/sentiment/{ticker}")
def sentiment_for_ticker(ticker: str):
    return get_news_sentiment(ticker)