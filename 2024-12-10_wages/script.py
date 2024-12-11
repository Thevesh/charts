import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from datetime import datetime


def heatmap():
    df = pd.read_excel('sgu.xlsx')
    df.age = (df.age.astype(str) + ' ').replace('nan ', '')
    df = df.set_index('age')

    sb.set(font="Monospace")
    fig, ax = plt.subplots(figsize=[10,7])  # width, height

    # heatmap
    sb.heatmap(df,
            annot=True, fmt=",.0f",
            annot_kws={'fontsize': 9},
            cmap='Blues',
            cbar=False,
            cbar_kws={"shrink": .9}, ax=ax)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_facecolor('white')
    ax.set_title(f'Median Wage by Age Group (2010-2023)\n', fontsize=10.5, linespacing=2)

    # ticks
    plt.yticks(rotation=0)
    ax.tick_params(axis=u'both', which=u'both',
                length=0, labelsize=10, 
                labelbottom=False, labeltop=True,
                bottom=False, top=False)
    
    ALT = 1
    if ALT == 1:
        # Print values for each row
        for idx, row in df.iterrows():
            print(f"\nAge group {idx}:")
            for year, value in row.items():
                print(f"{year}: {value:,.0f}")

    plt.savefig('wages.webp', dpi=400, bbox_inches='tight')


def timeseries():
    df = pd.read_excel('sgu.xlsx',sheet_name='ts').set_index('year')
    for c in df.columns: df[c] = df[c].pct_change() * 100
    df = df.dropna()
    df.columns = ['Median Wage Growth','Inflation']


    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    VAR = list(df.columns)
    COLOUR = ['red','black']

    for v,c in zip(VAR,COLOUR):
        df.plot(y=v,ax=ax,color=c,marker='o',markersize=4,lw=1,label=f'{v.title()}')

    # plot-wide adjustments
    ax.set_title(f"""Median Wage Growth vs Inflation (2011-2023)\n\n""")
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('#cccccc')
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.set_ylabel('',linespacing=0.5)
    ax.yaxis.grid(True,alpha=0.3)
    ax.set_ylim(-15.2,10)
    ax.yaxis.set_ticks(np.arange(-15, 10, 2.5))
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.1f')))

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.3)

    # legend
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.07), ncol=3)

    # special annotation
    for v,c in zip(VAR,COLOUR):
        ax.annotate(f'{v.title()}',(2026.5,df[v].iloc[-1]-0.3),color=c,fontsize=9.5,ha='center')

    # ALT-text copied directly to clipboard
    ALT = ''
    for i in range(len(df)):
        ALT += f"\n{i+2011}: " + ", ".join(f"{df[v].iloc[i]:.1f}" for v in VAR)
    print(ALT)

    plt.savefig('wages_v_prices.webp', dpi=400, bbox_inches='tight')


if __name__ == '__main__':
    print('')
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('\nGenerating timeseries:')
    timeseries()
    print('\nGenerating heatmap:')
    heatmap()
    print('')