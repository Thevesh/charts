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
    COLOUR = ['black','red']

    for v,c in zip(VAR,COLOUR):
        df.plot(y=v,ax=ax,color=c,marker=None,markersize=4,lw=1,label=f'{v.title()}')

    # plot-wide adjustments
    ax.set_title(f"""EPF Dividend Rate: 1952 to 2024\nLatest (2024): 6.30% for both Types\n""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('#cccccc')
    ax.set_axisbelow(True)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.04), ncol=2)

    # y-axis adjustments
    ax.set_ylabel('',linespacing=0.5)
    ax.yaxis.grid(True,alpha=0.25)
    ax.set_ylim(2,9)
    ax.yaxis.set_ticks(np.arange(2, 9, 0.5))
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.1f')))

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.25)
    ax.set_xlim(1950,2026)
    ax.xaxis.set_ticks(np.arange(1950, 2026, 5))

    # ALT-text copied directly to clipboard
    import pyperclip
    ALT = ''
    for i in range(len(df)):
        ALT += f"\n{df.index[i]}: " + ", ".join(f"{df[v].iloc[i]:.2f}" if pd.notna(df[v].iloc[i]) else "" for v in VAR)
    pyperclip.copy(ALT)

    for ext in ['png','webp']: plt.savefig(f'epf_dividend.{ext}',dpi=400)


if __name__ == '__main__':
    print(f'\nStart: {datetime.now():%Y-%m-%d %H:%M:%S}\n')
    df = pd.read_csv('dividend.csv').sort_values(by='year').set_index('year')
    df.columns = ['Conventional','Shariah']
    print('Generating timeseries chart')
    timeseries(df)
    print(f'\nEnd: {datetime.now():%Y-%m-%d %H:%M:%S}\n')
