# If not already installed, do: pip install pandas fastparquet
import pandas as pd
from datetime import date,timedelta
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import matplotlib.dates as mdates
import os


def timeseries():

    URL_DATA = 'https://storage.data.gov.my/demography/births.parquet'
    df = pd.read_parquet(URL_DATA).drop('state',axis=1)
    df = df[pd.to_datetime(df.date).dt.year >= 2000]
    df = df[pd.to_datetime(df.date).dt.year < 2023]

    df['date'] = '2015' + df.date.astype(str).str[4:]
    df = df[df.date != '2015-02-29']
    df = df.groupby('date').sum().reset_index()

    df.date = pd.to_datetime(df.date).dt.date - timedelta(280)
    df.date = '2014' + df.date.astype(str).str[4:]
    df['date'] = pd.to_datetime(df.date)

    df = df.sort_values(by='date').reset_index(drop=True)
    df['date_birth'] = pd.to_datetime(df.date).dt.date + timedelta(280)
    df = df.set_index('date')
    df['births_7d'] = df.births.rolling(7).mean()

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(y='births_7d',ax=ax,color='red')

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: Number of Babies Conceived on each Date
    (using daily births data from 2000-2022)
    (assuming pregnancy = 280 days)""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.5)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.set_ylim(29500,35500)
    ax.yaxis.set_label_coords(-0.02,1.02)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.setp(ax.get_xticklabels()[-1], visible=False)

    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())

    plt.savefig(f'timeseries.png',dpi=400)
    plt.close()


CURDIR = os.getcwd()
os.chdir(f'{CURDIR}/2024-02-14_valentines/')

print('')
timeseries()
print('')

os.chdir(CURDIR)