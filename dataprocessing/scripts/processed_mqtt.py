import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import Dash
#import numpy as np
from django.core.cache import cache
from .centralize import Centralized


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('processed_mqtt', external_stylesheets=external_stylesheets)
#app = Dash('processed_mqtt', external_stylesheets=external_stylesheets)

data = {
    'time': [],
    'Drehmoment': [],
    'Position': [],
    'Kraft': []
}

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
            max_intervals=1000
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    lon = cache.get('/test/sin/value')
    lat = cache.get('/test/cos/value')
    style = {'padding': '15px', 'fontSize': '16px'}
    return [
        html.Span('Sine signal: {0:.2f} '.format(lon), style=style),
        html.Span('Cosine signal: {0:.2f} '.format(lat), style=style),
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # Collect data
    origin_sin= Centralized(cache.get('/test/sin'),'sin')
    origin_cos= Centralized(cache.get('/test/cos'),'cos')
    opc_sin = cache.get('/opc/sin')


    data['Drehmoment'] = origin_sin.GenerateProcessedData()
    data['Position'] = origin_cos.GenerateProcessedData()
    data['time'] = [x * 0.1 for x in range(0, 100)]
        #np.linspace(0, 10, 100)

    # Create the graph with subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.2,
        subplot_titles=('Sin Signal', 'Cos Signal'),
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    #fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

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
    fig['layout']['xaxis']['title'] = 'Time (s)'
    fig['layout']['xaxis2']['title'] = 'Time (s)'
    fig['layout']['yaxis']['title'] = 'Sin Signal'
    fig['layout']['yaxis2']['title'] = 'Cos Signal'

    fig.update_layout(
        height=600,
        showlegend=False,
        title_text="Mqtt Test Signal",
        #xaxis_title='Time (s)',
        #yaxis_title='Sinus signal'
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
