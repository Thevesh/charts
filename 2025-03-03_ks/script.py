import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from datetime import datetime


def timeseries(df=None):

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [7.5,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    VAR = list(df.columns)
    COLOUR = ['red']

    for v,c in zip(VAR,COLOUR):
        df.plot(y=v,ax=ax,color=c,marker=None,markersize=4,lw=1,label=f'{v.title()}')

    # plot-wide adjustments
    ax.set_title(f"""Keluar Sekejap: Views by Episode\nNote: Removed 3 outliers for better visibility\nOutliers were Sanusi (1.9M), Tun M (2.4M) and TMJ (2.7M)""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('#cccccc')
    ax.set_axisbelow(True)
    ax.legend().set_visible(False)

    # y-axis adjustments
    ax.set_ylabel('',linespacing=0.5)
    ax.yaxis.grid(True,alpha=0.25)
    ax.set_ylim(0,1.05e6)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.25)
    ax.set_xlim(0,150)

    for ext in ['png','webp']: plt.savefig(f'ks_views.{ext}',dpi=400)


if __name__ == '__main__':
    print(f'\nStart: {datetime.now():%Y-%m-%d %H:%M:%S}\n')
    df = pd.read_csv('ks_views.csv')
    df = df[df.views < 1.1e6].set_index('episode')
    print('Generating timeseries chart')
    timeseries(df)
    print(f'\nEnd: {datetime.now():%Y-%m-%d %H:%M:%S}\n')
