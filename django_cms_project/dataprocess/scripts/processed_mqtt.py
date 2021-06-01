import dash_core_components as dcc
import datetime
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from django.core.cache import cache
from .centralize import Centralized



nodeDo = "ns=2;s=Demo.Dynamic.Scalar.Double"
nodeFl = "ns=2;s=Demo.Dynamic.Scalar.Float"
nodeIn = "ns=2;s=Demo.Dynamic.Scalar.Int32"
Server = 'opc.tcp://localhost:48010'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('processed_mqtt', external_stylesheets=external_stylesheets)
# app = dash.Dash('SecondExample', external_stylesheets=external_stylesheets)

data = {
    'time': [],
    'Drehmoment': [],
    'Position': [],
    'Kraft': []
}

# satellite = Orbital('TERRA')
num = 0
app.layout = html.Div(
    html.Div([
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            disabled=False,
            interval=2 * 1000,  # in milliseconds
            n_intervals=0,
            max_intervals=100
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    #Doubledata = opc(server, address1,'double')
    #Floatdata = opc(server, address2,'float')
    #lon = Doubledata.GetData().value
    #lat = Floatdata.GetData().value
    lon = cache.get('/test/sin/value')
    lat = cache.get('/test/cos/value')
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Drehmoment: {0:.2f} N/m'.format(lon), style=style),
        html.Span('Position: {0:.2f} m'.format(lat), style=style),
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # Collect data
    origin_sin= Centralized(cache.get('/test/sin'),'sin')
    origin_cos= Centralized(cache.get('/test/cos'),'cos')


    data['Drehmoment'] = origin_sin.GenerateDataset()
    data['Position'] = origin_sin.GenerateDataset()
    data['time'] = np.linspace(0, 10, 100)

    # Create the graph with subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.03,
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.add_trace(
        go.Scatter(
            x=data['time'],
            y=data['Drehmoment'],
            mode="lines",
            name="Drehmoment"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=data['time'],
            y=data['Position'],
            mode="lines",
            name="Position"
        ),
        row=2, col=1
    )
    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="Mqtt Test Signal",
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
