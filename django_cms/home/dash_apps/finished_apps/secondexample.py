import dash_core_components as dcc
import datetime
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.figure_factory as ff
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#import dash

#from django_cms.home.dash_apps.finished_apps.Datenerfassung import opc as op
from home.dash_apps.finished_apps.Datenerfassung import CollectData as collect
from home.dash_apps.finished_apps.Datenvorverarbeitung import Datenprocessing as process

#import Datenerfassung.CollectData as collect
#from pyorbital.orbital import Orbital

nodeDo = "ns=2;s=Demo.Dynamic.Scalar.Double"
nodeFl = "ns=2;s=Demo.Dynamic.Scalar.Float"
nodeIn = "ns=2;s=Demo.Dynamic.Scalar.Int32"
Server = 'opc.tcp://localhost:48010'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SecondExample', external_stylesheets=external_stylesheets)
#app = dash.Dash('SecondExample', external_stylesheets=external_stylesheets)

data = {
    'time': [],
    'Drehmoment': [],
    'Position': [],
    'Kraft': []
}

#satellite = Orbital('TERRA')
num = 0
app.layout = html.Div(
    html.Div([
        dcc.Dropdown(
            id='ProtocolType',
            #style={'columnCount': 2}
            options=[
                {'label': 'OPC UA', 'value': 'opc'},
                {'label': 'MQTT', 'value': 'mqtt'},
                {'label': 'REST', 'value': 'rest'}
            ],
            value='opc'
        ),
        dcc.Input(id="server", type="text", placeholder="Server",value="opc.tcp://localhost:48010",style = {'padding': '5px', 'fontSize': '16px'}),
        dcc.Input(id="address1", type="text", placeholder="Address",value="ns=2;s=Demo.Dynamic.Scalar.Double",debounce=True),
        dcc.Input(id="address2", type="text", placeholder="Address",value="ns=2;s=Demo.Dynamic.Scalar.Float",debounce=True),
        html.Button('Update', id='submit-val', n_clicks=0),
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


@app.callback(Output('live-update-text', 'children'),
              [Input('ProtocolType', 'value'),
               Input('server', 'value'),
               Input('address1', 'value'),
               Input('address2', 'value'),
               Input('interval-component', 'n_intervals')])
def update_metrics(protocol,server,address1,address2,n):
    Doubledata = collect.SensorData(protocol, server, address1)
    Floatdata = collect.SensorData(protocol, server, address2)
    Intdata = collect.SensorData(protocol, Server, nodeDo)
    lon = Doubledata.getData()
    lat = Floatdata.getData()
    alt = Intdata.getData()
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Drehmoment: {0:.2f} N/m'.format(lon), style=style),
        html.Span('Position: {0:.2f} m'.format(lat), style=style),
        html.Span('Kraft: {0:0.2f} N'.format(alt), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('ProtocolType', 'value'),
               Input('interval-component', 'n_intervals')])
def update_graph_live(protocol,n):
    # Collect data
    Doubledata = collect.SensorData(protocol, Server, nodeDo)
    Floatdata = collect.SensorData(protocol, Server, nodeFl)

    #Intdata = collect.SensorData(protocol, Server, nodeDo)

    lon = Doubledata.getData()
    lat = Floatdata.getData()
    #alt = Intdata.getData()

    data['Drehmoment'].append(lon)
    data['Position'].append(lat)
    data['time'].append(n)
    average = process.Datenprocessing(data['Drehmoment'],data['Position'])
    data['Kraft'] = average.Average(average.CombineData())

    # Create the graph with subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.03,
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}],
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
    fig.add_trace(
        go.Scatter(
            x=data['time'],
            y=data['Kraft'],
            mode="lines",
            name="Kraft"
        ),
        row=3, col=1
    )
    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="aktuelle Wert nach der Zeit",
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)