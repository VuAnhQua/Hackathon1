import yfinance as yf

listOfStock = {"MSFT", "AAPL"}
listOfStuffToGet = {"dividendRate", "dividendYield", "country", "industry", "dayHigh", "dayLow", "open", "previousClose", "volume", "allTimeHigh", "currentPrice", "targetHighPrice", "targetLowPrice", "recommendationKey", "fiftyTwoWeekRange", "displayName"}
for x in listOfStock:
    ticker = yf.Ticker(x)
    data = ticker.info
    news = ticker.news
    # print(data)
    tempStr = ""
    for y in listOfStuffToGet:
        tempStr += y + ": " + str(data[y])
        if y.find("Yield"):
            # tempStr += "%"
            pass
        tempStr += "\n"
    print("Stock: " + x + "\n" + tempStr + "\n")
    print(news)
