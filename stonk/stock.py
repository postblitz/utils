class Stock:
    def __init__(self, name, price, eps, shares, dividend):
        self.name = name
        self.price = price
        self.shares = shares
        self.market_cap = self.shares.all_shares * self.price
        self.dividend = dividend


class StockShares:
    def __init__(self, float, outstanding, shorted):
        self.tradeable_shares = float
        self.all_shares = outstanding
        self.shorted_shares = shorted


class StockPrice:
    def __init__(self, open_price, closing_price, eps):
        self.open_price = open_price
        self.closing_price = closing_price
        self.eps = eps
        self.pe = self.closing_price / self.pe

    def get_pe(self, live_price):
        return (live_price * self.pe) / self.closing_price
