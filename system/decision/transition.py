
class Transition:
    
    def __init__(self, signal, current_asset_position):
        self.signal = signal
        self.current_asset_position = current_asset_position
        
    def get_in(self):
        if self.current_asset_position == 0 and self.signal == "LONG":
            return ("Open", "LONG")
        elif self.current_asset_position == 0 and self.signal == "SHORT":
            return ("Open", "SHORT")
        else:
            return False

        
    def get_out(self):
        if self.current_asset_position == 1 and self.signal is None:
            return ("Close", "LONG")
        elif self.current_asset_position == -1 and self.signal is None:
            return ("Close", "SHORT")
        elif self.current_asset_position == -1 and self.signal == "LONG":
            return ("Close", "SHORT")
        elif self.current_asset_position == 1 and self.signal == "SHORT":
            return ("Close", "LONG")
        else:
            return False
        
        
    def get_skip(self):
        if self.signal == "LONG" and self.current_asset_position == 1:
            return ("-", "LONG")
        elif self.signal == "SHORT" and self.current_asset_position == -1:
            return ("-", "SHORT")
        else:
            return False
        
    def perform(self):
        self.get_in()
        self.get_out()
        
        self.get_pass()
        
        
