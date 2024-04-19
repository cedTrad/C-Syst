

class ProfitManager:
    def __init__(self, profit_target_percentage, trailing_stop_percentage):
        self.profit_target_percentage = profit_target_percentage
        self.trailing_stop_percentage = trailing_stop_percentage
        self.entry_price = None
        self.profit_target_price = None
        self.trailing_stop_price = None

    def set_entry_price(self, entry_price):
        self.entry_price = entry_price
        self.profit_target_price = entry_price * (1 + self.profit_target_percentage)
        self.trailing_stop_price = entry_price * (1 - self.trailing_stop_percentage)

    def take_profit(self, current_price):
        if current_price >= self.profit_target_price:
            return True
        return False

    def trailing_stop_loss(self, current_price):
        if current_price >= self.trailing_stop_price:
            self.trailing_stop_price = current_price * (1 - self.trailing_stop_percentage)
        return self.trailing_stop_price

