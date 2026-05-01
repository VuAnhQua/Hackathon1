from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/stocks")
def get_stocks():
    listOfStock = ["MSFT", "AAPL"]

    listOfStuffToGet = [
        "dividendRate", "dividendYield", "country", "industry",
        "dayHigh", "dayLow", "open", "previousClose", "volume",
        "currentPrice", "targetHighPrice", "targetLowPrice",
        "recommendationKey", "fiftyTwoWeekRange", "displayName"
    ]

    result = []

    for x in listOfStock:
        ticker = yf.Ticker(x)
        data = ticker.info

        stock_data = {}

        for y in listOfStuffToGet:
            stock_data[y] = data.get(y, "N/A")

        result.append({
            "ticker": x,
            "data": stock_data,
            "news": ticker.news
        })

    return result
