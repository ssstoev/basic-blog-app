import dash
import dash_bootstrap_components as dbc
from dash import html
from dash_app.layout import create_layout
import dash_app.callbacks

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL], title="My First Blog FastAPI App")

# Define the layout of the app
app.layout = create_layout()

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
