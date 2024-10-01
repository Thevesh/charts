import pandas as pd
import pyperclip
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def timeseries():
    df = pd.read_excel('lifetables.xlsx')
    df.date = pd.to_datetime(df.date).dt.year
    df = df[df.date >= 1970]
    dfs = {
        'female': df[df.sex == 'female'].copy().set_index('date'),
        'male': df[df.sex == 'male'].copy().set_index('date')
    }

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [8,8]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    ETHNIC = ['chinese','bumi','indian']
    SEX = ['female','male']
    COLOUR = ['red','black','blue']

    for e,c in zip(ETHNIC,COLOUR):
        for s in SEX:
            MARK = 'o' if s == 'female' else 'x'
            MARKERSIZE = 3 if s == 'female' else 4
            dfs[s].plot(y=e,ax=ax,color=c,marker=MARK,markersize=MARKERSIZE,lw=1,label=f'{e.title()} ({s.title()})')

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: Life Expectancy at Birth (1970-2024)\n\n""")
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.set_ylabel('Life Expectancy at Birth (Years)\n',linespacing=0.5)
    ax.yaxis.grid(True,alpha=0.3)
    ax.set_ylim(58,82)
    ax.yaxis.set_ticks(np.arange(60, 81, 5))
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.3)
    ax.set_xlim(1969,2028)
    ax.xaxis.set_ticks(np.arange(1970, 2024, 5).tolist() + [2024])

    # legend
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3)

    # special annotation
    for e,c in zip(ETHNIC,COLOUR):
        for s in SEX:
            ax.annotate(f'{s.title()}\n{e.title()}',(2026.5,dfs[s][e].iloc[-1]-0.3),color=c,fontsize=9.5,ha='center')

    # ALT-text copied directly to clipboard
    ALT = 'F = Female, M = Male   |   B = Bumi, C = Chinese, I = Indian\n'
    for i in [1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]:
        ALT += f"\n{i}: " + ", ".join(f"{dfs[s][e].loc[i]} ({s[0].upper()}-{e[0].upper()})" for s in SEX for e in ETHNIC)
    print(f"ALT char count: {len(ALT)}\n")
    print(ALT)

    plt.savefig('timeseries.png',dpi=400)
    plt.close()


if __name__ == '__main__':
    print('')
    timeseries()
    print('')