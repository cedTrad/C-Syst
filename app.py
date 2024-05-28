import dash
import dash_bootstrap_components as dbc
from app.layout import create_layout
from app.callbacks import register_callbacks
from app.db_utils import init_db

# Initialiser la base de données
init_db()

# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Définir la mise en page de l'application
app.layout = create_layout()

# Enregistrer les callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
    