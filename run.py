import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

import plot_apps

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        figure=plot_apps.find_where()
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)