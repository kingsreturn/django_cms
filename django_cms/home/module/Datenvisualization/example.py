import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import numpy as np
from django.core.cache import cache

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('example', external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H1('Square Root Slider Graph'),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    ),
])


@app.callback(
               Output('slider-graph', 'figure'),
              [Input('slider-updatemode', 'value')])
def display_value(value):
    x_axis = np.linspace(0, 10, 100)

    y_axis = cache.get('/test/sin')

    '''    
    fig = go.Figure(
        data=[go.scatter(x=x_axis,y=y_axis)],
        layout=layout
    )'''

    graph = go.Scatter(
        x=x_axis,
        y=y_axis,
        name='Manipulate Graph'
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
    )
    return {'data': [graph], 'layout': layout}
