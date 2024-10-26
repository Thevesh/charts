import pandas as pd
import numpy as np
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def timeseries(SCALED=0):
    gp = pd.read_parquet('https://storage.dosm.gov.my/gdp/gdp_gni_annual_nominal.parquet')
    gp = gp[gp['series'] == 'abs'][['date','gdp']]

    df = pd.read_excel('budget.xlsx')[['date','total']]
    df = pd.merge(df,gp,on='date',how='left')
    df.date = pd.to_datetime(df.date).dt.year
    repl = {2023:1895253, 2024:2065130, 2025:2220284}
    for k,v in repl.items():
        df.loc[df['date'] == k, 'gdp'] = v
    df.gdp = df.gdp * 1000000

    if SCALED == 0:
        df['budget_gdp'] = (df.total / 1e9).round(1)
    else:
        df['budget_gdp'] = (df.total / df.gdp * 100).round(1)
    df = df.set_index('date')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(y='budget_gdp',ax=ax,marker='.',color='red',lw=1,markersize=4)

    # conditional stuff

    # plot-wide adjustments
    if SCALED == 0:
        ax.set_title(f"Malaysia: Annual Announced Budget\n(1972-2025)",linespacing=1.8)
    else:
        ax.set_title(f"""Malaysia: Annual Announced Budget\nas % of Nominal GDP (1972-2025)\n(note: 2024-25 uses latest IMF GDP forecasts)""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    if SCALED == 0:
        ax.set_ylabel('RM bil',rotation=0,ha='center')
        ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f') + ''))
    else:
        ax.set_ylabel('%',rotation=0,ha='center')
        ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f') + '%'))
    ax.yaxis.grid(True,alpha=0.4)
    ax.yaxis.set_label_coords(-0.02,1.02)
    ax.set_ylim(0)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.4)
    ax.set_xlim(1970,2026)
    ax.set_xticks(np.arange(1970,2026,5))

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df.index[i]}: {df["budget_gdp"].iloc[i]:,.1f}')

    SUFFIX = 'scaled' if SCALED == 1 else 'unscaled'
    plt.savefig(f'timeseries_{SUFFIX}.webp',dpi=400)
    plt.close()


if __name__ == '__main__':
    print(''    )
    timeseries(SCALED=0)
    print('')
    timeseries(SCALED=1)
    print('')
