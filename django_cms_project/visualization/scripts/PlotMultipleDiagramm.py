# -*- coding: utf-8 -*-
# @Project: webframework_wenfengyang
# @Date    : 2021/6/2
# @Author  : Wenfeng
# @FileName: PlotMultipleDiagramm.py
# @contact : wenfengyangchn@gmail.com

import numpy as np
import matplotlib.pyplot as plt

import plotly.graph_objs as go
from plotly.offline import plot
import logging
from plotly.subplots import make_subplots
from scipy import fftpack
from django.core.cache import cache


logger = logging.getLogger(__name__)


def plot_linie(title,x_dataset,x_name,y_dataset,y_name):
    x_data = np.array(x_dataset)
    y_data = np.array(y_dataset)

    row=x_data.ndim

    fig = make_subplots(
        rows=row, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
    )

    for index in range(0,row):
        trace = go.scatter(
            x=x_data[index],
            y=y_dataset[index],
            mode='line',
            name=x_name[index]
        )
        fig.add_trace(trace)

    # Edit the layout
    fig.update_layout(title=title,
                      xaxis_title='Time (s)',
                      yaxis_title='Sensor data')

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
