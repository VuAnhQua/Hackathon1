import yfinance as yf


def get_stock_data(ticker_symbol: str, amount: float):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info

    return {
        "ticker": ticker_symbol.upper(),
        "amount": amount,
        "price": data.get("currentPrice", 0),
        "sector": data.get("sector", "Unknown"),
        "company_name": data.get("displayName", ticker_symbol.upper())
    }