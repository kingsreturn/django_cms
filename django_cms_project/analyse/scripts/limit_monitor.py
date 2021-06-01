# -*- coding: utf-8 -*-
# @Project: webframework_wenfengyang
# @Date    : 2021/5/31
# @Author  : Wenfeng
# @FileName: limit_monitor.py
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

class LimitMonitoring:
    def __init__(self,x_dataset,x_name,y_dataset,y_name):
        self.x_dataset=x_dataset
        self.x_name=x_name
        self.y_dataset=y_dataset
        self.y_name=y_name

    def plot_limit(self):
        x_data = np.linspace(0,10,100)
        y_data = cache.get('/test/sin')
        #above_limit= np.where(y_data >= 9)
        #below_limit= np.where(y_data <= 9)
        size = len(x_data)
        limit = np.full(size,9)

        fig = go.Figure()

        trace1 = go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines',
            name="Vibration"
        )
        trace2 = go.Scatter(
            x=x_data,
            y=limit,
            mode='lines',
            name="limit",
            #xaxis='frequency (Hz)'
        )

        fig.add_trace(trace1)
        fig.add_trace(trace2)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        logger.info("Plotting number of points {}.".format(len(x_data)))
        return plot_div

if __name__ == "__main__":
    pass
