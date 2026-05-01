
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
#yfinance is used to get stock data from Yahoo Finance
import yfinance as yf 

#This creates our app (this is the backend engine)
app = FastAPI()

#This defines ONE portfolio item (like AAPL - $2000)
class PortfolioItem(BaseModel):
  ticker: str #stock symbol (like AAPL)
  amount: float #how much money the user invested 

#This defines the FULL request (a list of stocks)
class PortfolioRequest(BaseModel):
  portfolio: List[PortfolioItem] #list of portfolio items

#This is a simple test route
#Frontened will send portfolio data here
@app.post("/analyze")
def analyze_portfolio(request: PortfolioRequest):
  #This list will store processed stock data
  results = []
  #Loop through each stock user sent
  for item in request.portfolio:
    # Get stock data from Yahoo Finance using ticker (like AAPl)
    stock = yf.Ticker(item.ticker)
    #Get detailed info about the stock
    info = stock.info
    #try to get sector (Technology, Finance, etc.) If not found, use "Unknown."
    sector = info.get("sector", "Unknown")
    #Try to get current price, if not found, use 0
    price = info.get("currentPrice", 0)
    #Add this stock's data to results list 
    results.append({
      "tickker": item.ticker, 
      "amount": item.amount,
      "sector": sector,
      "price": price
    })

#ADD up total money invested 
total_value = sum(item.amount for item in request.portfolio)

#Send everythig back to frontend
return {
  "total_value": total_value, # total portfolio value
  "portfolio": results #all stock data 
}


