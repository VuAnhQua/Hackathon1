from fastapi import FastAPI

from models import PortfolioRequest
from market import get_stock_data
from risk import calculate_risk
from ai import generate_ai_summary

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.post("/analyze")
def analyze_portfolio(request: PortfolioRequest):
    portfolio_results = []

    for item in request.portfolio:
        stock_data = get_stock_data(item.ticker, item.amount)
        portfolio_results.append(stock_data)

    risk_result = calculate_risk(portfolio_results)

    ai_summary = generate_ai_summary(portfolio_results, risk_result)

    return {
        "portfolio": portfolio_results,
        "risk": risk_result,
        "ai_summary": ai_summary
    }