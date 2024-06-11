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





def generate_flow_chart(wallet_balance, margin_balance, available_balance, 
                        unrealized_profit, initial_margin, 
                        open_order_initial_margin, position_initial_margin):
    """
    Génère un diagramme de flux interactif pour suivre les variables de portefeuille de futures.
    
    :param wallet_balance: Valeur de Wallet Balance
    :param margin_balance: Valeur de Margin Balance
    :param available_balance: Valeur de Available Balance
    :param unrealized_profit: Valeur de Unrealized Profit
    :param initial_margin: Valeur de Initial Margin
    :param open_order_initial_margin: Valeur de Open Order Initial Margin
    :param position_initial_margin: Valeur de Position Initial Margin
    """
    
    labels = [
        "Wallet Balance", "Margin Balance", "Available Balance", 
        "Unrealized Profit", "Initial Margin", 
        "Open Order Initial Margin", "Position Initial Margin"
    ]

    sources = [
        0,  # Wallet Balance to Margin Balance
        1,  # Margin Balance to Available Balance
        1,  # Margin Balance to Unrealized Profit
        2,  # Available Balance to Initial Margin
        3,  # Unrealized Profit to Margin Balance
        4,  # Initial Margin to Margin Balance
        4,  # Initial Margin to Open Order Initial Margin
        4   # Initial Margin to Position Initial Margin
    ]

    targets = [
        1,  # Wallet Balance to Margin Balance
        2,  # Margin Balance to Available Balance
        3,  # Margin Balance to Unrealized Profit
        4,  # Available Balance to Initial Margin
        1,  # Unrealized Profit to Margin Balance
        1,  # Initial Margin to Margin Balance
        5,  # Initial Margin to Open Order Initial Margin
        6   # Initial Margin to Position Initial Margin
    ]

    values = [
        wallet_balance,  # Wallet Balance to Margin Balance
        margin_balance,  # Margin Balance to Available Balance
        margin_balance,  # Margin Balance to Unrealized Profit
        available_balance,  # Available Balance to Initial Margin
        unrealized_profit,  # Unrealized Profit to Margin Balance
        initial_margin,  # Initial Margin to Margin Balance
        open_order_initial_margin,  # Initial Margin to Open Order Initial Margin
        position_initial_margin  # Initial Margin to Position Initial Margin
    ]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color="blue"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            customdata=values,
            hovertemplate='Value: %{value}<br />Source: %{source.label}<br />Target: %{target.label}<extra></extra>',
            color="lightblue"
        )
    ))

    fig.update_layout(title_text="Flow Chart of Futures Portfolio Variables", font_size=10)
    return fig

