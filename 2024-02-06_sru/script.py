import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import os


def timeseries():
    SRC = 'https://storage.dosm.gov.my/labour/lfs_qtr_sru_age.parquet'

    df = pd.read_parquet(SRC)
    df.date = pd.to_datetime(df.date)
    df = df[(df.variable == 'rate') & (df.age.isin(['15-24','25-34']))].drop('variable',axis=1).pivot(index='date',columns='age',values='sru')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [7,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    var = var_title = ['15-24','25-34'] # df col names 
    var_colour = ['red','black'] # plot colours
    var_lspace = [0.95,0.95] # adjustment for line label

    for v,c in zip(var,var_colour): df.plot(y=v,ax=ax,color=c,marker='.')

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: Skills-Related Underemployment for Youth\n(% of people with tertiary educ working in 'low/semi-skilled' job)""",linespacing=2)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, '.0f')))
    ax.set_ylim(20,79)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xticks(np.array(df.index.tolist()))

    # annotations
    for v,t,l,c in zip(var,var_title,var_lspace,var_colour): ax.annotate(t + 'yo',(df.index[-1],df[v].iloc[-1]*l),color=c,fontsize=8.8)
    for v,c in zip(var,var_colour):
        for i in range(len(df)):
            if i not in [6,26]: continue
            VAL = df[v].iloc[i]
            VAL_ADJ = VAL*1.035 if VAL < 50 else VAL*1.02
            HA = 'left'
            ax.annotate(f'{VAL:.1f}%',(df.index[i],VAL_ADJ),color=c,fontsize=8.8,ha=HA)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df.index[i]:%Y-%m}: {df["15-24"].iloc[i]:.1f}%, {df["25-34"].iloc[i]:.1f}%\n')

    plt.savefig(f'timeseries.png',dpi=400)
    plt.close()


CURDIR = os.getcwd()
os.chdir(f'{CURDIR}/2024-02-06_sru/')

print('')
timeseries()
print('')

os.chdir(CURDIR)