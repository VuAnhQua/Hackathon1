from pydantic import BaseModel
from typing import List

class PortfolioItem(BaseModel):
    ticker: str
    amount: float


class PortfolioRequest(BaseModel):
    portfolio: List[PortfolioItem]
