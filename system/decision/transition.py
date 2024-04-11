
class Transition:
    
    def __init__(self, signal, current_asset_position : int, risk_signal = ""):
        self.signal = signal
        self.current_asset_position = current_asset_position
        
    def get_in(self):
        if self.current_asset_position == 0 and self.signal == "LONG":
            return True, ("Open", "LONG")
        elif self.current_asset_position == 0 and self.signal == "SHORT":
            return True, ("Open", "SHORT")
        else:
            return False, ("", "")

        
    def get_out(self):
        if self.current_asset_position == 1 and self.signal is None:
            return True, ("Close", "LONG")
        elif self.current_asset_position == -1 and self.signal is None:
            return True, ("Close", "SHORT")
        elif self.current_asset_position == -1 and self.signal == "LONG":
            return True, ("Close", "SHORT")
        elif self.current_asset_position == 1 and self.signal == "SHORT":
            return True, ("Close", "LONG")
        else:
            return False, ("", "")
        
        
    def resize(self):
        return
        
        
    def skip(self):
        if self.signal == "LONG" and self.current_asset_position == 1:
            return True, ("-", "LONG")
        elif self.signal == "SHORT" and self.current_asset_position == -1:
            return True, ("-", "SHORT")
        else:
            return False, ("", "")
        
    

        
        
