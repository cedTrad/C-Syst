import dash
import dash_bootstrap_components as dbc
from app.layout import create_layout
from app.callbacks import CallBack
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='trading_app.log')

cb = CallBack()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.15.4/css/all.css"], suppress_callback_exceptions=True)
app.layout = create_layout()

cb.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
