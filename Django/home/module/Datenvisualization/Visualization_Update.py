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
import dash

# from django_cms.home.dash_apps.finished_apps.Datencollection import opc as op
#from home.module.Datencollection.opc import Opc as opc
#from home.module.Datenprocessing.Datenprocessing import Datenprocessing as process


nodeDo = "ns=2;s=Demo.Dynamic.Scalar.Double"
nodeFl = "ns=2;s=Demo.Dynamic.Scalar.Float"
nodeIn = "ns=2;s=Demo.Dynamic.Scalar.Int32"
Server = 'opc.tcp://localhost:48010'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('autoupdate', external_stylesheets=external_stylesheets)
#app = dash.Dash('SecondExample', external_stylesheets=external_stylesheets)

data = {
    'time': [],
    'sin': [],
    'cos': [],
    'sawtooth': []
}

# satellite = Orbital('TERRA')
num = 0
app.layout = html.Div(
    html.Div([
        html.Div(style={'marginLeft':70},id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            disabled=False,
            interval=0.5 * 1000,  # in milliseconds
            n_intervals=0,
            max_intervals=400
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    sin = cache.get('/test/sin/value')
    cos = cache.get('/test/cos/value')
    sawtooth = cache.get('/test/sawtooth/value')
    print(sin)

    style = {'padding': '5px', 'fontSize': '30px'}
    return [
        html.Span('Real Time Signal Value: ', style={'padding': '5px','fontSize':'34px'}),
        html.Br(),
        html.Span('sin : {0:.2f}'.format(sin), style=style),
        html.Span('cos : {0:.2f}'.format(cos), style=style),
        html.Span('sawtooth : {0:.2f}'.format(sawtooth), style=style),
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    data['sin'] = cache.get('/test/sin')
    data['cos'] = cache.get('/test/cos')
    data['time'] = np.linspace(0, 10, 100)
    #average = process(data['sin'], data['cos'])
    data['sawtooth'] = cache.get('/test/sawtooth')

    # Create the graph with subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.1,
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.add_trace(
        go.Scatter(
            x=data['time'],
            y=data['sin'],
            mode="lines",
            name="sin"
        ),
        row=1, col=1
    ),
    fig.add_trace(
        go.Scatter(
            x=data['time'],
            y=data['cos'],
            mode="lines",
            name="cos"
        ),
        row=2, col=1
    ),
    fig.add_trace(
        go.Scatter(
            x=data['time'],
            y=data['sawtooth'],
            mode="lines",
            name="cos"
        ),
        row=3, col=1
    )
    fig.update_layout(
        height=800,
        showlegend=False,
        title_font={
            'family': "Arial",
            'size': 34,
        },
        title={
            'text': "MQTT Test Signal",
            # 'title_font_size': 20,
            'y': 0.95,
            'x': 0.08,
            'xanchor': 'left',
            'yanchor': 'top'
        }
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
