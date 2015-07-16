from settings import ACCESS_TOKEN, ACCOUNT_ID
import oandapy


class Portfolio():
    def __init__(self, status):
        status["open_position"] = False
        status["position"] = 0
        self.unit = 1000
        self.status = status

        status["opening_price"] = 0
        status["executed_price"] = 0
        status["unrealized_pnl"] = 0
        status["realized_pnl"] = 0

        self.oanda = oandapy.API("practice", ACCESS_TOKEN)

    def update_portfolio(self, event):
        # Update position upon successful order
        if event.side == "buy":
            self.status["position"] += self.unit
        else:
            self.status["position"] -= self.unit

        if self.status["position"] == 0:
            self.status["open_position"] = False
            self.calculate_realized_pnl(event)
        else:
            self.status["opening_price"] = self.status["executed_price"]
            self.status["open_position"] = True

    def calculate_realized_pnl(self, event):
        self.status["unrealized_pnl"] += self.unit * (
            (self.status["opening_price"] - self.status["executed_price"])
            if event.side == "buy" else
            (self.status["executed_price"] - self.status["opening_price"]))

    def calculate_unrealized_pnl(self, event):
        if self.status["open_position"]:
            # Retrieve position from server
            pos = self.oanda.get_position(ACCOUNT_ID,
                                          event.instrument)
            units = pos["units"]
            side = pos["side"]
            avg_price = float(pos["avgPrice"])

            self.status["unrealized_pnl"] = units * (
                (event.bid - avg_price)
                if (side == "buy")
                else (avg_price - event.ask))
        else:
            self.status["unrealized_pnl"] = 0
