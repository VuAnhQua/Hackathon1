def calculate_risk(portfolio):
    total_value = sum(stock["amount"] for stock in portfolio)

    sector_totals = {}

    for stock in portfolio:
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
        "sector_allocation": sector_allocation,
        "risk_level": risk_level,
        "diversification_score": diversification_score
    }