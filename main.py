from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import yfinance as yf

app = FastAPI()

# -----------------------------
# Models
# -----------------------------
class PortfolioItem(BaseModel):
    ticker: str
    amount: float

class PortfolioRequest(BaseModel):
    portfolio: List[PortfolioItem]


# -----------------------------
# Stock Class (merged logic)
# -----------------------------
class Stock:
    def __init__(self, listOfStock: list, listOfStuffToGet: list):
        self.listOfStock = listOfStock
        self.listOfStuffToGet = listOfStuffToGet

    def get_data(self, with_news: bool = False):
        results = []

        for symbol in self.listOfStock:
            ticker = yf.Ticker(symbol)
            data = ticker.info

            stock_data = {}
            for field in self.listOfStuffToGet:
                stock_data[field] = data.get(field, "N/A")

            stock_result = {
                "ticker": symbol,
                "data": stock_data
            }

            # Optional news
            if with_news:
                stock_result["news"] = [
                    {
                        "summary": n.get("content", {}).get("summary", ""),
                        "date": n.get("content", {}).get("pubDate", ""),
                        "link": n.get("content", {}).get("canonicalUrl", {}).get("url", "")
                    }
                    for n in ticker.news
                ]

            results.append(stock_result)

        return results


# -----------------------------
# API Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/stocks")
def get_stocks():
    stock_obj = Stock(
        ["MSFT", "AAPL"],
        [
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
    )

    return stock_obj.get_data(with_news=False)


@app.post("/analyze")
def analyze_portfolio(request: PortfolioRequest):
    results = []

    total_value = 0

    for item in request.portfolio:
        ticker = yf.Ticker(item.ticker)
        data = ticker.info

        price = data.get("currentPrice", 0)
        total_value += price * item.amount

        results.append({
            "ticker": item.ticker.upper(),
            "amount": item.amount,
            "price": price,
            "sector": data.get("sector", "Unknown"),
            "company_name": data.get("displayName", item.ticker.upper()),
            "value": price * item.amount
        })

    return {
        "total_value": total_value,
        "portfolio": results
    }


# -----------------------------
# Optional standalone usage (like your original script)
# -----------------------------
if __name__ == "__main__":
    obj1 = Stock(
        ["MSFT", "AAPL"],
        ["dividendRate", "currentPrice", "industry"]
    )
    print(obj1.get_data(with_news=False))

    obj2 = Stock(
        ["AAPL"],
        ["currentPrice"]
    )
    print(obj2.get_data(with_news=False))
