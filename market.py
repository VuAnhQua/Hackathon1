import yfinance as yf

# Period can only be 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
# Interval can only be 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 4h, 1d, 5d, 1wk, 1mo, 3mo
def get_stock_data(ticker_symbol: str, amount: float, PeriodRange="1mo", IntervalRange="1d"):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info

    return {
        "ticker": ticker_symbol.upper(),
        "amount": amount,
        "price": data.get("currentPrice", 0),
        "sector": data.get("sector", "Unknown"),
        "company_name": data.get("displayName", ticker_symbol.upper()),
        "dividends": data.get("dividendYield"),
        "past_data": ticker.history(period=PeriodRange, interval=IntervalRange)
    }

# You can get open, volume, high, low data. (Ex: get_stock_data("AAPL", 5, "3mo")["past_data"]["Open"])
