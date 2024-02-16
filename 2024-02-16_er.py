import pandas as pd
from dateutil.relativedelta import relativedelta
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

PATH = '2024-02-16_er'

countries = {
    "myr_thb": "Thailand",
    "myr_eur": "Euro Area",
    "myr_usd": "USA",
    "myr_rmb": "China",
    "myr_jpy": "Japan",
    "myr_idr": "Indonesia",
    "myr_hkd": "Hong Kong",
    "myr_sgd": "Euro Area",
    "myr_twd": "Singapore",
    "myr_krw": "Taiwan",
    "myr_vnd": "Vietnam",
    "myr_inr": "India",
    "myr_aud": "Australia",
    "myr_php": "Philippines",
    "myr_aed": "UAE",
    "myr_sar": "Saudi Arabia",
    "myr_try": "Turkey",
    "myr_gbp": "UK",
    "myr_brl": "Brazil",
    "myr_mxn": "Mexico",
    "myr_bdt": "Bangladesh",
    "myr_chf": "Switzerland",
    "myr_cad": "Canada",
    "myr_rub": "Russia"
}


def bar():
    df = pd.read_parquet('https://storage.data.gov.my/finsector/exchangerates.parquet')
    DATE_E = df.date.iloc[-1]
    DATE_S = DATE_E - relativedelta(years=1)
    df = df[df.date >= DATE_S].set_index('date')

    # create percentage changes relative to first date
    df = df.multiply(1/np.array(list(df.iloc[0])), axis='columns')
    df = (df - 1)*100
    df = df.loc[[DATE_E]].transpose()
    df.columns = ['performance']
    df = df.sort_values(by='performance')
    df.index = [countries[x] if x in countries.keys() else x for x in df.index.tolist()]
    df = df[~df.index.isin(['Turkey','Russia'])] # Outliers and irrelevants

    plt.rcParams.update({'font.size': 10,
                        'font.family':'sans-serif',
                        'grid.linestyle': 'dotted',
                        'figure.figsize': [5,9],
                        'figure.autolayout': True})
    fig, ax = plt.subplots()

    n_pos = len(df[df.performance >= 0])
    n_neg = len(df[df.performance < 0])
    col_pos = sb.color_palette('Greens',n_colors=n_pos).as_hex()
    col_neg = sb.color_palette('Reds',n_colors=n_neg).as_hex()
    col_neg.reverse()

    v = 'performance'
    df.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_neg+col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'Ringgit vs Currencies of Major Trading Partners\n% change from {DATE_S:%d %b %Y} to {DATE_E:%d %b %Y}\n',linespacing=1.8)
    for b in ['top','right','bottom','left']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')
    ax.vlines(x=0,ymin=-1,ymax=22,colors=['gray'],linestyles=['dashed'],linewidth=0.7)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xlim(-22)
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f'{df[v].iloc[i]:,.1f}%  ' if i < 21 else f' +{df[v].iloc[i]:,.1f}%' for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=9)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip() + '\n')
        for i in range(len(df)):
            print(f'{i+1}) {df.index[len(df)-i-1]}: {labels[len(df)-i-1].strip()}')

    
    plt.savefig(f'output/{PATH}/bar.png',dpi=400)
    plt.close()


print('')
bar()
print('')