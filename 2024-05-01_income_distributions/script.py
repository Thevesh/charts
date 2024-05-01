import pandas as pd

import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def plot_distribution(
        df = None,
        COLOUR_UP = 'Greens',
        COLOUR_DOWN = 'Reds_r',
        TITLE_VAR = 'Income',
        TITLE_SCOPE = None, N_TOTAL = None,
        TITLE_CAVEAT = None,
        X_LABEL = '',
        SAVE_AS = ''
):
    if len(df)%2 == 0:
        col_up = sb.color_palette(COLOUR_UP, n_colors=int(len(df)/2)).as_hex()
        col_down = sb.color_palette(COLOUR_DOWN, n_colors=int(len(df)/2)).as_hex()
        SPLIT = int(len(df)/2)
    else:
        col_up = sb.color_palette(COLOUR_UP, n_colors=int(len(df)/2)).as_hex()
        col_down = sb.color_palette(COLOUR_DOWN, n_colors=int(len(df)/2)+1).as_hex()
        SPLIT = int(len(df)/2) + 1

    # plot chart
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(kind='barh', y=['n'], edgecolor='black', lw=0, ax=ax, legend=False)

    # custom bar colours
    for i, bar in enumerate(ax.patches):
        if i < SPLIT: bar.set_color(col_down[i])
        else: bar.set_color(col_up[i-SPLIT])

    # plot-wide adjustments
    ax.set_title(f'Monthly {TITLE_VAR} Distribution\nusing {N_TOTAL:,.0f} {TITLE_SCOPE}\n{TITLE_CAVEAT}',linespacing=1.8, fontsize=11)
    for b in ['top','right','left','bottom']: ax.spines[b].set_visible(False)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    ax.set_axisbelow(True)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.xaxis.grid(True,alpha=0.4)
    ax.set_xlabel(f'\n{X_LABEL}',linespacing=0.5)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(df)):
            print(f'{df.index[i]}: {df["n"].iloc[i]:.1f}%')

    plt.savefig(f'bar_{SAVE_AS}.png',dpi=400)
    plt.close()


if __name__ == '__main__':

    # ----- Household Income (DOSM) -----

    df = pd.read_parquet('https://storage.dosm.gov.my/hies/hies_malaysia_percentile.parquet')
    HOUSEHOLDS = 7909200
    df = df[(df.variable == 'maximum') & (df.date == df.date.max())][['income']].assign(n=HOUSEHOLDS/100)
    df['income'] = df['income'].fillna(40000)
    df.income  = (df.income / 1e3).round(0)
    df.loc[df.income > 20,'income'] = 20
    df = df.groupby('income').sum()
    df['n'] = df['n']/df['n'].sum() * 100
    df.index = ['< 1,000'] + [f'{x*1e3:,.0f} - {(x+1)*1e3-1:,.0f}' for x in range(1,len(df)-1)] + ['> 19,000']

    plot_distribution(df=df,
                    TITLE_SCOPE = 'households in 2022', N_TOTAL=HOUSEHOLDS,
                    TITLE_CAVEAT = '(note: household may have multiple incomes)',
                    X_LABEL = 'Proportion of Households (%)',
                    SAVE_AS='hies')


    # ----- Income Declarations (LHDN) -----

    df = pd.read_parquet('https://storage.data.gov.my/dashboards/incometax_interactive.parquet')
    df = df[(df.variable == 'income') & (df.state == 'Malaysia') & (df.type == 'all') & (df.age == 'all')][['value']].assign(n=41877)
    df = df[df.value != 0]
    FILINGS = df["n"].sum()
    df.value  = (df.value / 12e3).round(0)
    df.loc[df.value > 15,'value'] = 15
    df = df.groupby('value').sum()
    df['n'] = df['n']/df['n'].sum() * 100
    df.index = ['< 1,000'] + [f'{x*1e3:,.0f} - {(x+1)*1e3-1:,.0f}' for x in range(1,len(df)-1)] + ['> 15,000']

    plot_distribution(df=df,
                    COLOUR_UP = 'Blues',
                    TITLE_SCOPE = 'LHDN filings in 2022', N_TOTAL=FILINGS,
                    TITLE_CAVEAT = '(note: filings with income = 0 excluded)',
                    X_LABEL = 'Proportion of Tax Filings (%)',
                    SAVE_AS='lhdn')


    # ----- Formal Sector Wages (DOSM) -----

    df = pd.read_parquet('http://storage.dosm.gov.my/dashboards/labour_formalwages_snapshot_bracket.parquet')
    df.bracket = df.bracket.str.replace('RM ','').str.replace('RM','')
    df = df[df.date == df.date.max()].drop('date',axis=1).set_index('bracket').rename(columns={'n_people':'n'})
    WORKERS = df['n'].sum()
    df['n'] = df['n']/df['n'].sum() * 100

    plot_distribution(df=df,
                    TITLE_SCOPE = 'formal employees in Sep 2023', N_TOTAL=WORKERS,
                    TITLE_CAVEAT = '(note: does not include informal workers)',
                    X_LABEL = 'Proportion of Salary Recipients (%)',
                    SAVE_AS='formalwages')

