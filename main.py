from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import yfinance as yf

app = FastAPI()

class PortfolioItem(BaseModel):
    ticker: str
    amount: float

class PortfolioRequest(BaseModel):
    portfolio: List[PortfolioItem]

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/stocks")
def get_stocks():
    list_of_stock = ["MSFT", "AAPL"]

    fields_to_get = [
        "dividendRate",
        "dividendYield",
        "country",
        "industry",
        "dayHigh",
        "dayLow",
        "open",
        "previousClose",
        "volume",
        "currentPrice",
        "targetHighPrice",
        "targetLowPrice",
        "recommendationKey",
        "fiftyTwoWeekRange",
        "displayName"
    ]

    results = []

    for stock_symbol in list_of_stock:
        ticker = yf.Ticker(stock_symbol)
        data = ticker.info

        stock_data = {}

        for field in fields_to_get:
            stock_data[field] = data.get(field, "N/A")

        results.append({
            "ticker": stock_symbol,
            "data": stock_data
        })

    return results

@app.post("/analyze")
def analyze_portfolio(request: PortfolioRequest):
    results = []

    for item in request.portfolio:
        ticker = yf.Ticker(item.ticker)
        data = ticker.info

        results.append({
            "ticker": item.ticker.upper(),
            "amount": item.amount,
            "price": data.get("currentPrice", 0),
            "sector": data.get("sector", "Unknown"),
            "company_name": data.get("displayName", item.ticker.upper())
        })

    total_value = sum(item.amount for item in request.portfolio)

    return {
        "total_value": total_value,
        "portfolio": results
    }
