from binance.account import Future

class Portfolio:
    
    def __init__(self):
        self.account = Future()
        
    def futureAccount(self):
        account = self.account.info()
        
        itemsAccount = ['totalWalletBalance', 'totalUnrealizedProfit',
                 'totalMarginBalance', 'totalPositionInitialMargin',
                 'totalOpenOrderInitialMargin', 'availableBalance']
        
        itemsAsset = ['walletBalance', 'unrealizedProfit', 'positionInitialMargin',
                      'openOrderInitialMargin', 'availableBalance', 'updateTime']
        
        self.wallet = {
            'totalInitialMargin' : account['totalInitialMargin'],
            'totalMaintMargin' : account['totalMaintMargin'],
            'avaibleBalance' : account['availableBalance'],
            
            'totalWalletBalance' : account['totalWalletBalance'],
            'totalUnrealizedProfit' : account['totalUnrealizedProfit'],
            'totalMarginBalance' : account['totalMarginBalance'],
            
            'totalPositionInitialMargin' : account['totalPositionInitialMargin'],
            'totalOpenOrderInitialMargin' : account['totalOpenOrderInitialMargin']
        }
        
        self.assets = {}
        for asset in account['assets']:
            if float(asset['walletBalance']) != 0:
                temp = {key : asset[key] for key in itemsAsset}
                self.assets[asset['asset']] = temp
                
        
        items1 = ['initialMargin', 'maintMargin', 'unrealizedProfit', 'positionInitialMargin', 
                  'openOrderInitialMargin', 'positionAmt', 'entryPrice', 'leverage']
        
        items2 = ['markPrice' ,'notional', 'liquidationPrice', 'updateTime']
        
        self.positions = {}
        for position in account['positions']:
            if position['entryPrice'] != '0.0':
                temp = {key : position[key] for key in items1}
                self.positions[position['symbol']] = temp
        
        for symbol in self.positions.keys():
            self.positions[symbol]['size'] = float(self.positions[symbol]['entryPrice']) * float(self.positions[symbol]["positionAmt"])
            for key in items2:
                self.positions[symbol][key] = self.account.positionInfo(symbol)[0][key]
        
        return self.wallet, self.account
    