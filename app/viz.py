import plotly.graph_objects as go
import pandas as pd


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


def ohlc_fig(symbol, df_ohlc):
    ohlc_fig = go.Figure(data=[go.Candlestick(
                x=df_ohlc['time'],
                open=df_ohlc['open'],
                high=df_ohlc['high'],
                low=df_ohlc['low'],
                close=df_ohlc['close']
            )])
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

