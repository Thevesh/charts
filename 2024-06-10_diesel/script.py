import pandas as pd
import numpy as np
import seaborn as sb
from datetime import datetime, date
from dateutil.relativedelta import relativedelta as rd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def timeseries():
    df = pd.DataFrame(columns=['year','total','diesel'])
    for y in range(2000,2025):
        tf = pd.read_parquet(f'https://storage.data.gov.my/catalogue/cars_{y}.parquet',
                            columns=['fuel'])
        df.loc[len(df)] = [
            y,
            len(tf),
            len(tf[tf.fuel.str.contains('diesel')])
        ]
    df['proportion'] = (df.diesel / df.total) * 100

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    # plot
    df.plot(y='proportion',ax=ax,color='red',marker='o',markersize=3)

    # plot-wide adjustments
    ax.set_title(f"""JPJ Car Registrations: 2000 to 2024 (30 Apr)
    % of Cars using a Diesel Engine""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.5)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.set_ylim(0,11)
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 1))

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.5)
    ax.set_xlim(1999,2024.2)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f"{df.index[i]}: {df['proportion'].iloc[i]:,.1f}%")

    plt.savefig(f'timeseries.png',dpi=400)
    plt.close()


def bar():
    df = pd.DataFrame(columns=['model'])
    for y in range(2020,2025):
        tf = pd.read_parquet(f'https://storage.data.gov.my/catalogue/cars_{y}.parquet',
                            columns=['maker','model','fuel'])
        tf = tf[tf.fuel.str.contains('diesel')].drop('fuel',axis=1)
        tf['model'] = tf.maker + ' ' + tf.model
        tf = tf.drop('maker',axis=1)
        df = pd.concat([df,tf],axis=0,ignore_index=True)
    df = df.groupby('model').size().to_frame('vehicles').reset_index()

    df.model = df.model.str.title().str.replace('Cx-','CX-')
    df = df.set_index('model')
    df['perc'] = (df.vehicles / df.vehicles.sum()) * 100
    df = df[df.vehicles >= 1000].sort_values(by='vehicles')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'vehicles'
    col_pos = sb.color_palette('Reds', n_colors=len(df)).as_hex()
    df.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'Most Popular Diesel Car Models\nJan 2020 to Apr 2024',linespacing=2,fontsize=11)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f"  {df[v].iloc[i]:,.0f}  ({df['perc'].iloc[i]:,.1f}%)" for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(df)):
            print(f'{i+1}) {df.index[len(df)-i-1]}: {labels[len(df)-i-1].strip()}')

    plt.savefig(f'bar.png',dpi=400)
    plt.close()


if __name__ == '__main__':
    timeseries()
    bar()
