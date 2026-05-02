from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import PortfolioRequest
from market import get_stock_data
from risk import calculate_risk
from ai import generate_ai_summary, generate_ai_recommendations
from sentiment import get_news_sentiment


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "wealth-management-backend",
    }


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
        ai_summary = "AI temporarily unavailable. Please try again later."

    try:
        recommendations = generate_ai_recommendations(portfolio_results, risk_result)
    except Exception:
        recommendations = []

    if not recommendations:
        recommendations = []

        for stock in portfolio_results:
            sentiment = stock.get("sentiment", {}).get("sentiment", "Neutral")
            ticker = stock["ticker"]

            if sentiment == "Positive":
                action = "BUY"
                confidence = 75
                reason = f"{ticker} has positive recent news sentiment."
            elif sentiment == "Negative":
                action = "SELL"
                confidence = 70
                reason = f"{ticker} has negative recent news sentiment."
            else:
                action = "HOLD"
                confidence = 60
                reason = f"{ticker} has neutral recent news sentiment."

            recommendations.append({
                "symbol": ticker,
                "action": action,
                "confidence": confidence,
                "reason": reason,
                "priceTarget": "N/A",
            })

    total_value = sum(stock["amount"] for stock in portfolio_results)

    dashboard = {
        "totalValue": total_value,
        "riskLevel": risk_result.get("risk_level"),
        "diversificationScore": risk_result.get("diversification_score"),
        "sectorAllocation": risk_result.get("sector_allocation"),
    }

    return {
        "portfolio": portfolio_results,
        "risk": risk_result,
        "dashboard": dashboard,
        "recommendations": recommendations,
        "ai_summary": ai_summary,
    }


@app.get("/stocks")
def get_stocks():
    default_tickers = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "NVDA",
        "TSLA",
        "AMZN",
        "META",
        "JPM",
    ]

    results = []

    for ticker in default_tickers:
        stock_data = get_stock_data(ticker, 0)
        sentiment_data = get_news_sentiment(ticker)

        stock_data["sentiment"] = sentiment_data
        results.append(stock_data)

    return results


@app.get("/stock/{ticker}")
def get_single_stock(ticker: str):
    stock_data = get_stock_data(ticker, 0)
    sentiment_data = get_news_sentiment(ticker)

    stock_data["sentiment"] = sentiment_data

    return stock_data


@app.get("/news/{ticker}")
def get_news_for_ticker(ticker: str):
    return get_news_sentiment(ticker)