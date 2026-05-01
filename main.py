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
