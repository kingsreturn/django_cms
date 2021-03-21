import dash_core_components as dcc
import time
import datetime
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objs as go
import plotly.express as px
from django_plotly_dash import DjangoDash

from home.dash_apps.finished_apps import opc as op
#import opc as op
#from pyorbital.orbital import Orbital

nodeDo = "ns=2;s=Demo.Dynamic.Scalar.Double"
nodeFl = "ns=2;s=Demo.Dynamic.Scalar.Float"
nodeIn = "ns=2;s=Demo.Dynamic.Scalar.Int32"
ServerName = 'opc.tcp://localhost:48010'
opcObject = op.GetDataFromOpcServer(ServerName=ServerName, NodeID=nodeDo)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SecondExample', external_stylesheets=external_stylesheets)
#app = dash.Dash('SecondExample', external_stylesheets=external_stylesheets)

#satellite = Orbital('TERRA')
num = 0
app.layout = html.Div(
    html.Div([
        html.H1('Condition Monitoring'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            disabled=False,
            interval=1*1000, # in milliseconds
            n_intervals=0,
            max_intervals=100
        )
    ])
)

#@app.callback(Output('live-update-text', 'children'),
#              Input('interval-component', 'n_intervals'))
@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    #lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    lon = op.GetDataFromOpcServer(ServerName=ServerName, NodeID=nodeDo)
    lat = op.GetDataFromOpcServer(ServerName=ServerName, NodeID=nodeFl)
    alt = op.GetDataFromOpcServer(ServerName=ServerName, NodeID=nodeIn)
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Drehmoment: {0:.2f} N/m'.format(lon), style=style),
        html.Span('Position: {0:.2f} m'.format(lat), style=style),
        html.Span('Kraft: {0:0.2f} N'.format(alt), style=style)
    ]


# Multiple components can update everytime interval gets fired.
#@app.callback(Output('live-update-graph', 'figure'),
#              Input('interval-component', 'n_intervals'))
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    #satellite = Orbital('TERRA')
    data = {
        'time': [],
        'Drehmoment': [],
        'Position': [],
        'Kraft': []
    }

    # Collect some data
    #for i in range(180):
    time = datetime.datetime.now() - datetime.timedelta(seconds=2000)
    lon = op.GetDataFromOpcServer(ServerName=ServerName, NodeID=nodeDo)
    lat = op.GetDataFromOpcServer(ServerName=ServerName, NodeID=nodeFl)
    alt = op.GetDataFromOpcServer(ServerName=ServerName, NodeID=nodeIn)

    data['Drehmoment'].append(lon)
    data['Position'].append(lat)
    data['Kraft'].append(alt)
    data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['Drehmoment'],
        'name': 'Kraft',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['Position'],
        #'text': data['time'],
        'name': 'Position',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['Kraft'],
        #'text': data['time'],
        'name': 'Drehmoment',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)