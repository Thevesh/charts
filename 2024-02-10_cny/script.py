import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import os


def timeseries():
    df = pd.read_excel(f'src.xlsx').set_index('year')


    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5.5,5.5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(y='births',ax=ax,color='red',marker='.')

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: Chinese Births\nfrom 1998 to 2022\n""",linespacing=1.5)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.5)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.set_ylim(30001)
    ax.yaxis.set_label_coords(-0.02,1.02)

    # x-axis adjustments
    ax.set_xlabel('')
    # ax.set_xticks(np.array(df.index.tolist()))

    # annotations
    for v,c in zip(['births'],['red']):
        for i in range(len(df)):
            if i not in [2,14,24]: continue
            VAL = df[v].iloc[i]
            GRADIENT = 0 if i == 0 else (df[v].iloc[i]-df[v].iloc[i-1])/(df.index[i]-df.index[i-1])
            VAL_ADJ = VAL-5000 if GRADIENT < 0 else VAL+1500
            ax.annotate(f'{VAL/1000:.0f}k',(df.index[i],VAL_ADJ),color=c,fontsize=10,ha='center')

    # special annotation
    ax.annotate(f'2000: Year\nof the Dragon!',(2005,115000),color=c,fontsize=10,ha='center')
    ax.annotate(f'2012: Year\nof the Dragon!',(2017,88000),color=c,fontsize=10,ha='center')

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df.index[i]}: {df["births"].iloc[i]:,.0f} births')

    plt.savefig(f'timeseries.png',dpi=400)
    plt.close()


CURDIR = os.getcwd()
os.chdir(f'{CURDIR}/2024-02-10_cny/')

print('')
timeseries()
print('')

os.chdir(CURDIR)
