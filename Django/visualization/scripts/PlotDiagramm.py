# -*- coding: utf-8 -*-
# @Project: webframework_wenfengyang
# @Date    : 2021/6/2
# @Author  : Wenfeng
# @FileName: PlotDiagramm.py
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

class PlotDiagramm():
    def __init__(self,title,x_dataset,x_name,y_dataset,y_name):
        self.x_data = x_dataset
        self.y_data = y_dataset
        self.x_name = x_name
        self.y_name = y_name
        self.title = title

    def plot_linie(self):
        row=self.x_data.ndim

        fig = go.Figure()


        trace = go.Scatter(
            x=self.x_data,
            y=self.y_data,
            mode='lines',
            name=self.y_name
        )
        fig.add_trace(trace)

        # Edit the layout
        fig.update_layout(title=self.title,
                          xaxis_title=self.x_name,
                          yaxis_title=self.y_name)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        logger.info("Plotting number of points {}.".format(len(self.x_data)))
        return plot_div

    def plot_punkt(self,title,x_dataset,x_name,y_dataset,y_name):

        trace1 = go.Scatter(
            x=x_dataset,
            y=y_dataset
        )

        data = [trace1]
        layout = go.Layout(
            xaxis=dict(
                autorange=True
            ),
            yaxis=dict(
                autorange=True
            )
        )
        fig = go.Figure(data=data, layout=layout)

        # Edit the layout
        fig.update_layout(title=title,
                          xaxis_title=x_name,
                          yaxis_title=y_name)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        logger.info("Plotting number of points {}.".format(len(x_dataset)))
        return plot_div


if __name__ == "__main__":
    FastFourierTransformation.generateData()
    x_axis = cache.get('time')
    # print(time)
    y_axis = cache.get('signal')
    time = cache.get('time')
    # print(time)
    f_t = cache.get('signal')
    #plot_original()


    F = fftpack.fft(f_t)
    f = fftpack.fftfreq(100, 1.0 / 10)
    mask = np.where(f >= 0)
    fig, axes = plt.subplots(3, 1, figsize=(8, 6))
    # print(mask)

    axes[0].plot(f[mask], np.log(abs(F[mask])), label="real")
    axes[0].plot(5, 0, 'r*', markersize=10)
    axes[0].set_ylabel("$\log(|F|)$", fontsize=14)

    axes[1].plot(f[mask], abs(F[mask]) / 100, label="real")
    axes[1].set_xlim(0, 2.5)
    axes[1].set_ylabel("$|F|$", fontsize=14)

    axes[2].plot(f[mask], abs(F[mask]) / 100, label="real")
    axes[2].set_xlabel("frequency (Hz)", fontsize=14)
    axes[2].set_ylabel("$|F|$", fontsize=14)
    plt.show()

