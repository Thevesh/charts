import pandas as pd
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import os


def timeseries():
    URL = 'https://storage.dosm.gov.my/demography/death_maternal.parquet'

    df = pd.read_parquet(URL).set_index('date')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(y='rate',ax=ax,marker='.',color='red')

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: Maternal Mortality Rate from 1946 to 2022
Maternal death = died during pregnancy / childbirth
The rates are per 100,000 births""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.4)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.yaxis.set_label_coords(-0.02,1.02)
    # ax.set_ylim(-10,10)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.4)

    # annotations
    ax.annotate(f'In 1946, nearly 1 in every 100\npregnancies ended in death',xy=(date(1949,1,1),620),color='red',fontsize=10,linespacing=1.5,ha='left')
    ax.annotate(f'By 2022, that number went\ndown to just 1 in 4000',(date(2022,1,1),100),color='red',fontsize=10,linespacing=1.5,ha='right')

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df.index[i]:%Y}: {df["rate"].iloc[i]:,.1f}')

    plt.savefig(f'timeseries.png',dpi=400)
    plt.close()


CURDIR = os.getcwd()
os.chdir(f'{CURDIR}/2024-03-03_mmr/')

print('')
timeseries()
print('')

os.chdir(CURDIR)
