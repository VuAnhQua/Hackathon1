import yfinance as yf

listOfStock = {"MSFT", "AAPL"}
listOfStuffToGet = {"dividendRate", "dividendYield", "country", "industry", "dayHigh", "dayLow", "open", "previousClose", "volume", "allTimeHigh", "currentPrice", "targetHighPrice", "targetLowPrice", "recommendationKey", "fiftyTwoWeekRange", "displayName"}
for x in listOfStock:
    ticker = yf.Ticker(x)
    data = ticker.info
    news = ticker.news
    tempStr = ""
    # Get all data in listOfStuffToGet (Can add more)
    for y in listOfStuffToGet:
        tempStr += y + ": " + str(data[y])
        tempStr += "\n"
    print("Stock: " + x + "\n" + tempStr + "\n")
    # Get all news
    for y in news:
        print("Summary: "+ str(y["content"]["summary"]) + "\nDate: " + str(y["content"]["pubDate"]) + "\nLink:" + str(y["content"]["canonicalUrl"]["url"]))


# print(msft.financials)
