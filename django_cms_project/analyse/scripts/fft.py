import numpy as np
import matplotlib.pyplot as plt

import plotly.graph_objs as go
from plotly.offline import plot
import logging
from plotly.subplots import make_subplots
from scipy import fftpack
from django.core.cache import cache


logger = logging.getLogger(__name__)

class FastFourierTransformation:
    def __init__(self,x_dataset,x_name,y_dataset,y_name):
        self.x_dataset=x_dataset
        self.x_name=x_name
        self.y_dataset=y_dataset
        self.y_name=y_name

    def generateData(self):
        sampling = 100
        startpoint = 0
        endpoint = 10
        time = np.linspace(startpoint, endpoint, sampling)
        signal = (np.sin(1 * np.pi * time) + np.sin(2 * np.pi * time) + np.sin(4 * np.pi * time))
        cache.set('time',time,60)
        cache.set('signal', signal, 60)

    def plot_original(self):
        x_data = self.x_dataset
        y_data = self.y_dataset

        trace1 = go.Scatter(
            x=x_data,
            y=y_data
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
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        logger.info("Plotting number of points {}.".format(len(x_data)))
        return plot_div


    def plot_fft(self):
        size = len(self.x_dataset)
        periode = 0.1
        F = fftpack.fft(self.y_dataset)
        f = fftpack.fftfreq(size, periode)
        mask = np.where(f >= 0)

        x_data = f[mask]
        y_data1 = np.log(abs(F[mask]))
        y_data2 = abs(F[mask]) / 100

        trace1 = go.Scatter(
            x=x_data,
            y=y_data1,
            name="log(|F|)"
        )
        trace2 = go.Scatter(
            x=x_data,
            y=y_data2,
            name="|F|",
            #xaxis='frequency (Hz)'
        )

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            specs=[[{"type": "scatter"}],
                   [{"type": "scatter"}]]
        )

        fig.add_trace(trace1,row=1, col=1)
        fig.add_trace(trace2, row=2, col=1)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        logger.info("Plotting number of points {}.".format(len(x_data)))
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

