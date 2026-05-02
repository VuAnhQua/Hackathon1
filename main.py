from fastapi import FastAPI
import yfinance as yf

app = FastAPI()


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

        sector = data.get("sector", "Unknown")

        results.append({
            "ticker": item.ticker.upper(),
            "amount": item.amount,
            "price": data.get("currentPrice", 0),
            "sector": sector,
            "company_name": data.get("displayName", item.ticker.upper())
        })

    total_value = sum(item.amount for item in request.portfolio)

    sector_totals = {}

    for stock in results:
        sector = stock["sector"]
        amount = stock["amount"]

        if sector not in sector_totals:
            sector_totals[sector] = 0

        sector_totals[sector] += amount

    sector_allocation = {}

    for sector, amount in sector_totals.items():
        sector_allocation[sector] = round((amount / total_value) * 100, 2)

    highest_sector_percentage = max(sector_allocation.values())

    if highest_sector_percentage >= 60:
        risk_level = "High"
    elif highest_sector_percentage >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    diversification_score = round(100 - highest_sector_percentage, 2)

    return {
        "total_value": total_value,
        "portfolio": results,
        "sector_allocation": sector_allocation,
        "risk_level": risk_level,
        "diversification_score": diversification_score
    }

    {
  "portfolio": [
    {
      "ticker": "AAPL",
      "amount": 2000
    },
    {
      "ticker": "NVDA",
      "amount": 3000
    },
    {
      "ticker": "VOO",
      "amount": 5000
    }
  ]
}
