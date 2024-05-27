from dash import Dash
from app.layout import create_layout
from app.callbacks import register_callbacks

# Initialisation de l'application
app = Dash(__name__)

# Configuration de la mise en page
app.layout = create_layout()

# Enregistrement des callbacks
register_callbacks(app)

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)

