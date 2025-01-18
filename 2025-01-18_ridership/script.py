import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd


lines = ['rail_lrt_kj','rail_lrt_ampang','rail_mrt_kajang','rail_mrt_pjy','rail_monorail']

map_cols = {
    'rail_lrt_kj': 'LRT Kelana Jaya',
    'rail_lrt_ampang': 'LRT Ampang',
    'rail_mrt_kajang': 'MRT Kajang',
    'rail_mrt_pjy': 'MRT Putrajaya',
    'rail_monorail': 'Monorail'
}

line_assmt = {
    'rail_lrt_kj': '✕',
    'rail_lrt_ampang': '✕',
    'rail_mrt_kajang': '✓',
    'rail_mrt_pjy': '-',
    'rail_monorail': '✓'
}

map_month = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'
}

map_dow = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun'
}


def timeseries_combined(tf=None,TITLE=None,DIVISOR=1e3,UNIT='k',SAVE_AS=None):
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [8.5,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    VAR = lines
    COLOUR = ['red','blue','black','orange','#2ecc71']

    for v,c in zip(VAR,COLOUR): tf.plot(y=v,ax=ax,color=c,lw=1.2)

    # plot-wide adjustments
    ax.set_title(TITLE,linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('#cccccc')
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.set_ylabel('',linespacing=0.5)
    ax.yaxis.grid(True,alpha=0.3)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.3)
    # ax.set_xlim(tf.index.min(),tf.index.max()+rd(months=6))

    # special annotation
    for v,c in zip(VAR,COLOUR):
        SHIFT = 1.02 if v == 'rail_mrt_kajang' else 0.98 if v == 'rail_lrt_kj' else 1
        ax.annotate(f'   {map_cols[v]}: {tf[v].iloc[-1]/DIVISOR:,.1f}{UNIT}',(datetime(2024,12,31,0,0,0),tf[v].iloc[-1]*SHIFT),color=c,fontsize=10,ha='left')
    
    plt.savefig(f'{SAVE_AS}.png',dpi=400,bbox_inches='tight')
    plt.close()


def timeseries_split(tf=None,TITLE=None,SAVE_AS=None):

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [10,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,3)
    ax = ax.ravel()


    for a in range(6):
        LINE = a if a < 2 else a - 1
        SPACE = '' if a < 2 else '\n'
        COLOUR = 'red' if a < 2 else 'blue'
        if a == 2: 
            for b in ['top','right','left','bottom']: ax[a].spines[b].set_visible(False)
            ax[a].yaxis.set_visible(False)
            ax[a].xaxis.set_visible(False)
            continue

        tf.plot(y=lines[LINE], ax=ax[a], color=COLOUR,legend=False, lw=1)
        ax[a].set_title(f'{SPACE}{map_cols[lines[LINE]]}',linespacing=1.8)

        for b in ['top','right']: ax[a].spines[b].set_visible(False)
        for b in ['left','bottom']: ax[a].spines[b].set_color('#cccccc')
        ax[a].set_axisbelow(True)

        # y-axis adjustments
        ax[a].set_ylabel('',linespacing=0.5)
        ax[a].yaxis.grid(True,alpha=0.3)
        DP = ',.0f' if len(tf) < 10 else ',.1f'
        ax[a].get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, DP)))

        # x-axis adjustments
        ax[a].set_xlabel('')
        ax[a].xaxis.grid(True,alpha=0.3)

    plt.suptitle(TITLE)
    plt.savefig(f'{SAVE_AS}.png',dpi=400,bbox_inches='tight')
    plt.close()


def bar_day_of_week(tf=None,TITLE=None,SAVE_AS=None,MILLIONS=False):
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    if MILLIONS:
        plt.rcParams["figure.figsize"] = [11,8]
    else:
        plt.rcParams["figure.figsize"] = [9,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,2)
    ax = ax.ravel()

    lines_here = ['rail_lrt_kj','rail_lrt_ampang','rail_mrt_kajang','rail_monorail']
    for a in range(4):
        SPACE = '' if a < 2 else '\n'

        INDEX = 'month' if MILLIONS else 'day'
        tf[tf.line == lines_here[a]].set_index(INDEX).plot(kind='bar',y=['2019','2024'], color=['#041f61','orange'],ax=ax[a],legend=False, lw=1)
        ax[a].set_title(f'{SPACE}{map_cols[lines_here[a]]}',linespacing=1.8)

        for b in ['top','right']: ax[a].spines[b].set_visible(False)
        for b in ['left','bottom']: ax[a].spines[b].set_color('#cccccc')
        ax[a].set_axisbelow(True)

        # y-axis adjustments
        ax[a].set_ylabel('',linespacing=0.5)
        ax[a].yaxis.grid(True,alpha=0.3)
        if MILLIONS:
            ax[a].get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x/1e6, ',.1f') + ' mil'))
        else:
            ax[a].get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))

        # x-axis adjustments
        ax[a].set_xlabel('')
        ax[a].xaxis.grid(True,alpha=0.3)
        ax[a].tick_params(axis='x', rotation=0)

    plt.suptitle(TITLE,linespacing=1.8)
    bar_blue = plt.Rectangle((0,0), 1, 1, label='2019', color='#041f61')
    bar_orange = plt.Rectangle((0,0), 1, 1, label='2024', color='orange')
    LEGEND_VPOS = 0.95 if MILLIONS else 0.9
    fig.legend(ncol=2, handles=[bar_blue, bar_orange], bbox_to_anchor=(0.5, LEGEND_VPOS), loc='upper center')

    plt.savefig(f'{SAVE_AS}.png',dpi=400,bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    # We require these dataframes:
    # [df] Daily ridership data from data.gov.my
    # [dfmd] Avg daily ridership from 2019 to 2024
    # [dfmm] Monthly ridership from 2019 to 2024
    # [dfy] Annual ridership from 2019 to 2024
    # [dfmc] Ridership by month in 2019 vs 2024
    # [dfwc] Ridership by day of week in 2019 vs 2024

    df = pd.read_parquet(
        'https://storage.data.gov.my/transportation/ridership_headline.parquet',
        columns=['date',*lines]
    )
    df.date = pd.to_datetime(df.date)

    # --------- Monthly timeseries ---------

    print('\nProcessing monthly timeseries data')
    dfm = df.copy().fillna(0)
    dfm['date'] = pd.to_datetime(dfm['date'].astype(str).str[:7] + '-01')
    dfmd = dfm.groupby('date').mean().round(0).astype(int).reset_index() # FINAL: Monthly data, average daily ridership
    dfmm = dfm.groupby('date').sum().round(0).astype(int).reset_index() # FINAL: Monthly data, total ridership

    print('Chart: Monthly avg ridership (combined)')
    timeseries_combined(
        tf=dfmd.set_index('date'),
        TITLE='Average Daily Ridership on LRT, MRT, & Monorail (2019-2024)\n(note: daily avg helps account for diff N of days in each month)',
        DIVISOR=1e3,
        UNIT='k',
        SAVE_AS='timeseries_combined_monthly_avg'
    )

    print('Chart: Monthly total ridership (combined)')
    timeseries_combined(
        tf=dfmm.set_index('date'),
        TITLE='Monthly Ridership on LRT, MRT, & Monorail (2019-2024)\n(note: different N of days in months leads to fluctuations)',
        DIVISOR=1e6,
        UNIT='mil',
        SAVE_AS='timeseries_combined_monthly_total'
    )


    # --------- Annual timeseries ---------

    print('\nProcessing annual timeseries data')
    dfy = df[~df.date.astype(str).str.contains('02-29')].copy().fillna(0) # Exclude Feb 29th data
    dfy['date'] = pd.to_datetime(dfy['date'].astype(str).str[:4] + '-01-01')
    dfy = dfy.groupby('date').sum().round(0).astype(int).reset_index() # FINAL: Annual data, total ridership

    print('Chart: Monthly total ridership (split view)')
    timeseries_split(
        tf=dfmm.set_index('date')/1e6,
        TITLE='Monthly Ridership (millions) on LRT, MRT, & Monorail (2019-2024)',
        SAVE_AS='timeseries_split_monthly'
    )

    print('Chart: Annual total ridership (split view)')
    timeseries_split(
        tf=dfy.set_index('date')/1e6,
        TITLE='Annual Ridership (millions) on LRT, MRT, & Monorail (2019-2024)',
        SAVE_AS='timeseries_split_annual'
    )

    # --------- Bar charts for analysis ---------

    print('\nProcessing bar chart data')
    dfmc = dfmm[dfmm.date.dt.year.isin([2019,2024])].drop('rail_mrt_pjy',axis=1)
    dfmc['year'] = dfmc.date.dt.year.astype(str)
    dfmc = dfmc.melt(id_vars=['year','date'],value_vars=[x for x in lines if 'pjy' not in x],var_name='line',value_name='ridership')
    dfmc['date'] = dfmc.date.dt.strftime('%m')
    dfmc = dfmc.pivot_table(index=['line','date'],columns='year',values='ridership').reset_index().rename(columns={'date':'month'})
    dfmc['month'] = dfmc.month.map(map_month)
    for c in ['2019','2024']: dfmc[c] = dfmc[c].astype(int) # FINAL: Ridership by month in 2019 vs 2024

    dfwc = df[df.date.dt.year.isin([2019,2024])].copy().fillna(0).drop('rail_mrt_pjy',axis=1)
    dfwc['year'] = dfwc.date.dt.year.astype(str)
    dfwc['date'] = dfwc.date.dt.dayofweek
    dfwc = dfwc.groupby(['year','date']).mean().reset_index()
    dfwc = dfwc.melt(id_vars=['year','date'],value_vars=[x for x in lines if 'pjy' not in x],var_name='line',value_name='ridership')
    dfwc = dfwc.pivot(index=['line','date'],columns='year',values='ridership').reset_index().rename(columns={'date':'day'})
    dfwc['day'] = dfwc.day.map(map_dow)
    for c in ['2019','2024']: dfwc[c] = dfwc[c].astype(int) # FINAL: Ridership by day of week in 2019 vs 2024

    print('Chart: Ridership by day of week (2019 vs 2024)')
    bar_day_of_week(
        tf=dfwc,
        TITLE='Average Daily LRT, MRT, & Monorail Ridership\nby Day of Week\n',
        SAVE_AS='bar_dow'
    )

    print('Chart: Ridership by month (2019 vs 2024)')
    bar_day_of_week(
        tf=dfmc,
        TITLE='LRT, MRT, & Monorail Ridership by Month\n',
        SAVE_AS='bar_month',
        MILLIONS=True
    )

    print('')