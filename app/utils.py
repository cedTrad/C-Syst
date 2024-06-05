from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "QNTUSDT",
    "LTCBTC", "EGLDUSDT", "ONTUSDT"
]

dark_template = {
    "layout": {
        "paper_bgcolor": "black",        # Couleur de fond du papier
        "plot_bgcolor": "black",         # Couleur de fond de la zone de tracé
        "font": {
            "color": "white",            # Couleur des textes
            "size": 12,                  # Taille des textes
            "family": "Arial"            # Police des textes
        },
        "xaxis": {
            "showgrid": False,           # Suppression de la grille des axes x
            "zeroline": False,           # Suppression de la ligne zéro des axes x
            "color": "white",            # Couleur des lignes et des textes des axes x
            "tickcolor": "white"         # Couleur des ticks des axes x
        },
        "yaxis": {
            "showgrid": False,           # Suppression de la grille des axes y
            "zeroline": False,           # Suppression de la ligne zéro des axes y
            "color": "white",            # Couleur des lignes et des textes des axes y
            "tickcolor": "white"         # Couleur des ticks des axes y
        },
        "title": {
            "x": 0.5,                    # Positionnement du titre au centre
            "xanchor": "center"          # Ancrage du titre au centre
        }
    }
}




# ------------------ Portfolio overviews -----------------------------

def prisk(totalInitialMargin, totalWalletBalance, totalMaintMargin, totalUnrealizedProfit):
    leverage_ratio = round((totalInitialMargin / totalWalletBalance) * 100, 2) if totalWalletBalance != 0 else 0
    maint_margin_ratio = round((totalMaintMargin / totalWalletBalance) * 100, 2) if totalWalletBalance != 0 else 0
    risk_reward_ratio = round((totalUnrealizedProfit / totalInitialMargin) * 100, 2) if totalInitialMargin != 0 else 0
    return {"leverage_ratio" : leverage_ratio, "maint_margin_ratio" : maint_margin_ratio, "risk_reward_ratio" : risk_reward_ratio}


def waterfall(totalWalletBalance, totalInitialMargin, totalUnrealizedProfit, availableBalance):
    waterfall_fig = go.Figure(
        go.Waterfall(
            name="20", 
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Wallet Balance", "Initial Margin", "UPnL", "Available Balance"],
            text=[
                f"${totalWalletBalance:.3f}", 
                f"${totalInitialMargin:.3f}", 
                f"${totalUnrealizedProfit:.3f}", 
                f"${availableBalance:.3f}"
            ],
            y=[
                totalWalletBalance, 
                -totalInitialMargin, 
                totalUnrealizedProfit, 
                availableBalance
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "Maroon", "line": {"color": "red", "width": 2}}},
            increasing={"marker": {"color": "Teal"}}
        )
    )
    waterfall_fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.5),
        margin={'t': 0, 'b': 0, 'l': 10, 'r': 0},
        template="plotly_dark",  # assuming 'dark_template' is a predefined template
        showlegend=False,
        yaxis=dict(
            showticklabels=False,  # hide y-axis tick labels
            title='',             # remove y-axis title
            zeroline=False        # hide y-axis zero line
        ),
        xaxis=dict(
            tickfont=dict(size=10),  # reduce the font size of x-axis labels
            automargin=True          # adjust margins to fit labels
        )
    )
    return waterfall_fig


def portfolio_overviews(portfolio_data : dict):
    totalWalletBalance = float(portfolio_data['totalWalletBalance'])
    totalInitialMargin = float(portfolio_data['totalInitialMargin'])
    totalMaintMargin = float(portfolio_data['totalMaintMargin'])
    totalUnrealizedProfit = float(portfolio_data['totalUnrealizedProfit'])
    totalMarginBalance = float(portfolio_data['totalMarginBalance'])
    availableBalance = float(portfolio_data['availableBalance'])
    maxWithdrawAmount = float(portfolio_data['maxWithdrawAmount'])
    
    r_risk = prisk(totalInitialMargin, totalWalletBalance, totalMaintMargin, totalUnrealizedProfit)
    waterfall_fig = waterfall(totalWalletBalance, totalInitialMargin, totalUnrealizedProfit, availableBalance)
    return r_risk, waterfall_fig
    




# ----------------------- Positions -----------------------------

def update_position_state(symbol : str, positions_data : dict, open_orders_data : dict, get_price, ohlc_data):
    positions = []
    total_portfolio_value = 0  # Initialiser la valeur totale du portefeuille

    for pos in positions_data:
        if float(pos['positionAmt']) != 0:
            symbol = pos['symbol']
            current_price_data = get_price(symbol)
            current_price = float(current_price_data['price']) if 'price' in current_price_data else None
            position_amt = float(pos['positionAmt'])
            entry_price = float(pos['entryPrice'])
            unrealized_profit = float(pos['unRealizedProfit'])
            leverage = float(pos['leverage'])
                
            # Récupérer les ordres ouverts pour le symbole actuel
            stop_loss, take_profit = None, None
            for order in open_orders_data:
                if order['symbol'] == symbol:
                    if order['type'] == 'STOP_MARKET':
                        stop_loss = float(order['stopPrice'])
                    elif order['type'] == 'TAKE_PROFIT_MARKET':
                        take_profit = float(order['stopPrice'])

            # Calcul des nouvelles colonnes
            position_type = 'LONG' if position_amt > 0 else 'SHORT'
            roi = (unrealized_profit / (entry_price * abs(position_amt))) * leverage * 100 if entry_price != 0 else 0
            entry_amount = entry_price * abs(position_amt)
            current_value = current_price * abs(position_amt) if current_price is not None else 0
                
            total_portfolio_value += current_value
                
            positions.append({
                'symbol': symbol,
                'positionAmt': round(position_amt, 2),
                'entryPrice': round(entry_price, 2),
                'entryAmount': round(entry_amount, 2),
                'unrealizedProfit': round(unrealized_profit, 2),
                'leverage': round(leverage, 2),
                'currentValue': round(current_value, 2),
                'breakEvenPrice': round(entry_price, 2),  # Placeholder, update with correct calculation if available
                'stopLoss': round(stop_loss, 2) if stop_loss is not None else None,
                'takeProfit': round(take_profit, 2) if take_profit is not None else None,
                'positionType': position_type,
                'ROI (%)': round(roi, 2)
            })
    
    fig_ohlc = ohlc(positions, symbol, ohlc_data)        
    
    return positions, fig_ohlc






def ohlc(positions, symbol, ohlc_data):
    ohlc_fig = go.Figure()
    if symbol:
        
        if ohlc_data:
            # ------------ Traitement 
            df_ohlc = pd.DataFrame(ohlc_data, columns=["openTime", "open", "high", "low", "close", "volume", "time", "quoteAssetVol", "nbTrades", "takerBuyVol", "takerBuyQuote", "Ig"])
            df_ohlc['time'] = df_ohlc['time'].apply(lambda x : pd.to_datetime(x, unit='ms')) 
            df_ohlc["low"] = df_ohlc["low"].astype(float)
            df_ohlc["high"] = df_ohlc["high"].astype(float)
            df_ohlc["open"] = df_ohlc["open"].astype(float)
            df_ohlc["close"] = df_ohlc["close"].astype(float)
            
            ohlc_fig = go.Figure(data=[go.Candlestick(
                x=df_ohlc['time'],
                open=df_ohlc['open'],
                high=df_ohlc['high'],
                low=df_ohlc['low'],
                close=df_ohlc['close']
            )])
            # Ajouter des annotations pour les informations sur la position
            pos = next((p for p in positions if p['symbol'] == symbol), None)
            if pos:
                add_annotations(ohlc_fig, df_ohlc['time'], pos)
            
            max_time = df_ohlc['time'].max() + pd.Timedelta(hours=8)
            y_range = [min(df_ohlc["low"]) * 0.99, max(df_ohlc["high"]) * 1.01]
            ohlc_fig.update_yaxes(range=y_range, showgrid=False)
            ohlc_fig.update_xaxes(range=[df_ohlc['time'].min(), max_time], rangeslider_visible=False, showgrid=False,
                                  rangeselector=dict(
                                      buttons=[
                                          dict(count=30, label="30min", step="minute", stepmode="backward"),
                                          dict(count=4, label="4h", step="hour", stepmode="backward"),
                                          dict(count=12, label="12h", step="hour", stepmode="backward"),
                                          dict(count=1, label="1d", step="day", stepmode="backward"),
                                          dict(count=3, label="3d", step="day", stepmode="backward"),
                                          dict(count=7, label="7w", step="day", stepmode="backward")
                                      ],
                                      font=dict(color="blue")
                                  ))
            
            ohlc_fig.update_layout(
                height=600,
                legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.5),
                margin={'t': 0, 'b': 0, 'l': 10, 'r': 0},
                template=dark_template,
                showlegend=False
            )
    return ohlc_fig



def add_scatter(fig, data, feature, name, color = None, col = None, row = None):
    fig.add_trace(
        go.Scatter(
            x = data.index,
            y = data[feature],
            mode = 'markers',
            marker_color = color,
            name = name
        ),
        col = col, row = row
    )

def add_annotations(ohlc_fig, time_range, pos):
    ohlc_fig.add_trace(go.Scatter(
        x=[time_range.min(), time_range.max()],
        y=[pos['entryPrice'], pos['entryPrice']],
        mode="markers",
        name="Entry Price",
        line=dict(color="blue", width=2, dash="dash")
    ))
    if pos.get('stopLoss') is not None:
        ohlc_fig.add_trace(go.Scatter(
            x=[time_range.min(), time_range.max() + pd.Timedelta(hours=8)],
            y=[pos['stopLoss'], pos['stopLoss']],
            mode="lines",
            name="Stop Loss",
            line=dict(color="red", width=2, dash="dash")
        ))
    if pos.get('takeProfit') is not None:
        ohlc_fig.add_trace(go.Scatter(
            x=[time_range.min(), time_range.max() + pd.Timedelta(hours=8)],
            y=[pos['takeProfit'], pos['takeProfit']],
            mode="lines",
            name="Take Profit",
            line=dict(color="green", width=2, dash="dash")
        ))
    ohlc_fig.add_trace(go.Scatter(
        x=[time_range.min(), time_range.max() + pd.Timedelta(hours=8)],
        y=[pos.get('breakEvenPrice', pos['entryPrice'])],  # Utiliser entryPrice comme valeur de secours
        mode="lines",
        name="Break Even Price",
        line=dict(color="orange", width=2, dash="dash")
    ))

