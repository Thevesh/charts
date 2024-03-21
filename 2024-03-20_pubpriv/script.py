import pandas as pd
from datetime import date, datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import os


def timeseries():
    df = pd.read_csv('students.csv')
    df.date = pd.to_datetime(df.date)
    df = df.set_index('date')
    df['ratio'] = df.public/df.private

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,8]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,1)

    var = ['public','private']
    var_title = ['Gov','Private']
    var_c = ['blue','red']

    for i in [0,1]:
        df.plot(y=var[i],ax=ax[i],marker='.',color=var_c[i])

        # plot-wide adjustments
        ax[i].set_title(f"""Enrolment in {var_title[i]} Schools""",linespacing=1.8)
        for b in ['top','right']: ax[i].spines[b].set_visible(False)
        ax[i].set_axisbelow(True)
        ax[i].get_legend().remove()

        # y-ax[i]is adjustments
        ax[i].yaxis.grid(True,alpha=0.4)
        ax[i].get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))

        # x-ax[i]is adjustments
        ax[i].set_xlabel('')
        ax[i].xaxis.grid(True,alpha=0.4)
        ax[i].set_xlim(datetime(2002,1,1,0,0,0),datetime(2022,1,1,0,0,0))

    plt.suptitle('             Malaysia: Secondary Schools')

    # ALT-text
    ALT = 1
    if ALT == 1:
        for i in range(len(df)): print(f'{df.index[i]:%Y}: {df["public"].iloc[i]/1e6:,.2f}m gov, {df["private"].iloc[i]/1e3:,.0f}k private')
    
    plt.savefig(f'timeseries.png',dpi=400)
    plt.close()


def timeseries_ratio():
    df = pd.read_csv('students.csv')
    df.date = pd.to_datetime(df.date)
    df = df.set_index('date')
    df['ratio'] = df.public/df.private

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(y='ratio',ax=ax,marker='.',color='red')

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: Secondary Schools\nRatio of Gov School to Private Students\n""",linespacing=1.5)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.4)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.yaxis.set_label_coords(-0.02,1.02)
    ax.set_ylim(15,34)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.4)
    ax.set_xlim(datetime(2002,1,1,0,0,0),datetime(2022,1,1,0,0,0))

    # annotations
    ax.annotate(f'In 2005, gov school students\noutnumbered private by >30x',xy=(datetime(2004,1,1),32),color='red',fontsize=10,linespacing=1.5,ha='left')
    ax.annotate(f'By 2021, this fell\nto just over 20x',xy=(datetime(2022,6,1),20.8),color='red',fontsize=10,linespacing=1.5,ha='right')

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df.index[i]:%Y}: {df["ratio"].iloc[i]:,.1f}')

    plt.savefig(f'timeseries_ratio.png',dpi=400)
    plt.close()


CURDIR = os.getcwd()
os.chdir(f'{CURDIR}/2024-03-20_pubpriv/')

print('')
timeseries()
print('')
timeseries_ratio()
print('')

os.chdir(CURDIR)
