import numpy as np
import matplotlib.pyplot as plt

import plotly.graph_objs as go
from plotly.offline import plot
import logging
from plotly.subplots import make_subplots
from scipy import fftpack
logger = logging.getLogger(__name__)


def signal_samples(t):
    return np.sin(1 * np.pi * t) + np.sin(2 * np.pi * t) + np.sin(4 * np.pi * t)

def timesampling():
    sampling = 100
    startpoint = 0
    endpoint = 10
    time = np.linspace(startpoint,endpoint,sampling)
    return time

def frequenzsampling(time):
    return (np.sin(1 * np.pi * time) + np.sin(2 * np.pi * time) + np.sin(4 * np.pi * time))

B = 5
f_s = 10
N = 100
#print(N)

time = timesampling()
#print(time)
f_t = frequenzsampling(time)

def plot_original():
    x_data = timesampling()
    #print(x_data)
    # print(time)
    y_data = frequenzsampling(time)

    trace1 = go.Scatter(
        x=x_data,
        y=y_data
    )

    data = [trace1]
    layout = go.Layout(
        # autosize=False,
        # width=900,
        # height=500,

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


def plot_fft():
    F = fftpack.fft(f_t)
    f = fftpack.fftfreq(N, 1.0 / f_s)
    mask = np.where(f >= 0)
    fig, axes = plt.subplots(3, 1, figsize=(8, 6))

    x_data = f[mask]
    y_data1 = np.log(abs(F[mask]))
    y_data2 = abs(F[mask]) / N
    y_data3 = np.log(abs(F[mask]))

    trace1 = go.Scatter(
        x=x_data,
        y=y_data1
    )
    trace2 = go.Scatter(
        x=x_data,
        y=y_data2
    )

    #data = [trace1,trace2,trace3]
    layout = go.Layout(
        # autosize=False,
        # width=900,
        # height=500,

        xaxis=dict(
            autorange=True
        ),
        yaxis=dict(
            autorange=True
        )
    )
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.03,
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    fig.add_trace(trace1,row=1, col=1)
    fig.add_trace(trace2, row=2, col=1)
    #fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    logger.info("Plotting number of points {}.".format(len(x_data)))
    return plot_div

if __name__ == "__main__":
    time = timesampling()
    # print(time)
    f_t = frequenzsampling(time)
    #plot_original()


    F = fftpack.fft(f_t)
    f = fftpack.fftfreq(N, 1.0 / f_s)
    mask = np.where(f >= 0)
    fig, axes = plt.subplots(3, 1, figsize=(8, 6))
    # print(mask)

    axes[0].plot(f[mask], np.log(abs(F[mask])), label="real")
    axes[0].plot(B, 0, 'r*', markersize=10)
    axes[0].set_ylabel("$\log(|F|)$", fontsize=14)

    axes[1].plot(f[mask], abs(F[mask]) / N, label="real")
    axes[1].set_xlim(0, 2.5)
    axes[1].set_ylabel("$|F|$", fontsize=14)

    axes[2].plot(f[mask], abs(F[mask]) / N, label="real")
    axes[2].set_xlabel("frequency (Hz)", fontsize=14)
    axes[2].set_ylabel("$|F|$", fontsize=14)
    plt.show()

