import pandas as pd
from datetime import date

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import matplotlib.ticker as tkr
from matplotlib.ticker import FixedFormatter, FixedLocator


# this function is used to selectively keep the date labels on the x-axis
def keep_date(tdate, i, type, max=1):
        if type == '1m': 
             return tdate.strftime('%d-%b') if (i % 5 == 0 and max - i > 5) or i == max else ''
        elif type == '6m':
            return tdate.strftime('%d\n%b') if tdate.day == 1 else ''
        elif type == 'all':
            if tdate.day == 1:
                return tdate.strftime('%b\n%y') if tdate.month == 1 else tdate.strftime('%b') if tdate.month in [3, 5, 7, 9, 11] else ''
            else:
                return ''


# this function is used to generate the date labels on the x-axis, uses keep_date() to select
def gen_date_xticks(date_list, type):
    ticks_dates = [pd.to_datetime(x) for x in date_list]
    MAX = len(ticks_dates)-1
    ticks_dates.reverse()
    ticks_dates = [keep_date(ticks_dates[i], i, type, max=MAX) for i in range(len(ticks_dates))]
    ticks_dates.reverse()
    return ticks_dates


def make_data():
    df = pd.read_excel('padu.xlsx')
    df = df.sort_values(by=['date','state']).reset_index(drop=True)
    for c in df.columns[2:]: df[c] = pd.to_numeric(df[c],errors='coerce').fillna(0).astype(int)
    df = pd.concat([
        df.assign(state='Malaysia').groupby(['state','date']).sum().reset_index(),
        df],axis=0,ignore_index=True
    )
    df.loc[(df.state == 'Malaysia') & (df.date.dt.date < date(2024,1,7)),'reg_cumul'] = [0,186704,438387,567279,682355,747125] # no state level data before 7 Jan 2024
    for c in df.columns[2:]: df[c.replace('cumul','daily')] = df.groupby('state')[c].diff().fillna(df[c]).astype(int)
    df.to_parquet('padu.parquet',index=False,compression='brotli')


def timeseries_abs():
    df = pd.read_parquet('padu.parquet')
    df.date = pd.to_datetime(df.date)
    df = df[df.state == 'Malaysia'][['date','reg_daily','reg_cumul']]
    XTICKS = gen_date_xticks(df.date.tolist(),'1m')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [4.5,8]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,1)

    var = ['reg_daily','reg_cumul']
    var_title = ['PADU: Daily Registrations','\nPADU: Cumulative Registrations']
    var_callout = [f'\nTotal: {df[var[0]].sum():,.0f} ~ Yesterday: +{df[var[0]].iloc[-1]:,.0f}\n',
                '']

    for a in range(2):
        df.plot(y=var[a], ax=ax[a], color='blue')
        ax[a].set_title(f"""{var_title[a]}{var_callout[a]}""",linespacing=1.8)
        for b in ['top','right']: ax[a].spines[b].set_visible(False)
        ax[a].get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax[a].yaxis.grid(True)
        ax[a].set_axisbelow(True)
        ax[a].set_ylabel('')
        ax[a].set_xlabel('')
        ax[a].xaxis.set_ticks([x for x in range(len(df))])
        ax[a].xaxis.set_ticklabels(XTICKS)
        ax[a].tick_params(axis='both', which='both', length=0)
        ax[a].get_legend().remove()
        ax[a].xaxis.grid(True)
        ax[a].set_ylim(0.01)
        ax[a].set_xlim(0)

        xgridlines = ax[a].get_xgridlines()
        for i in range(len(XTICKS)): 
            if XTICKS[i] == '': xgridlines[i].set_visible(False)

    print(f'A vertical panel of 2 timeseries charts showing daily (top) and cumulative (bottom) registrations for PADU.\n\nData:')
    for i in range(1,len(df)): print(f'{df.date[i]:%d-%b}: {df["reg_cumul"].iloc[i]:,.0f} (+{df["reg_daily"].iloc[i]:,.0f})')

    plt.savefig('padu_1_ts_abs.webp',dpi=400)
    plt.close()


def timeseries_rate():
    df = pd.read_parquet('padu.parquet')
    df.date = pd.to_datetime(df.date)
    df = df[df.state == 'Malaysia'][['date','reg_daily','reg_cumul']]
    for c in df.columns[1:]: df[c.replace('reg','rate')] = df[c]/21754319 * 100
    XTICKS = gen_date_xticks(df.date.tolist(),'1m')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [4.5,8]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,1)

    var = ['rate_daily','rate_cumul']
    var_title = ['PADU: Daily Registration Rate\n(% of Citizens aged 18+)','\nPADU: Cumulative Registration Rate']
    var_callout = [f'\nOverall: {df[var[0]].sum():,.1f}% ~ Yesterday: +{df[var[0]].iloc[-1]:,.1f}%\n', '']

    for a in range(2):
        df.plot(y=var[a], ax=ax[a], color='red')
        ax[a].set_title(f"""{var_title[a]}{var_callout[a]}""",linespacing=1.8)
        for b in ['top','right']: ax[a].spines[b].set_visible(False)
        ax[a].get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.1f')))
        ax[a].yaxis.grid(True)
        ax[a].set_axisbelow(True)
        ax[a].set_ylabel('')
        ax[a].set_xlabel('')
        ax[a].xaxis.set_ticks([x for x in range(len(df))])
        ax[a].xaxis.set_ticklabels(XTICKS)
        ax[a].tick_params(axis='both', which='both', length=0)
        ax[a].get_legend().remove()
        ax[a].xaxis.grid(True)
        ax[a].set_ylim(0.01)
        ax[a].set_xlim(0)

        xgridlines = ax[a].get_xgridlines()
        for i in range(len(XTICKS)): 
            if XTICKS[i] == '': xgridlines[i].set_visible(False)

    print(f'A vertical panel of 2 timeseries charts showing daily (top) and cumulative (bottom) registrations for PADU as a % of citizens aged 18+.\n\nData:')
    for i in range(len(df)): print(f'{df.date[i]:%d-%b}: {df["rate_cumul"].iloc[i]:,.1f} (+{df["rate_daily"].iloc[i]:,.1f}%)')

    plt.savefig('padu_2_ts_rate.webp',dpi=400)
    plt.close()


def bar_abs():
    df = pd.read_parquet('padu.parquet',columns=['state','date','reg_cumul'])
    df = df[df.date.dt.date < date(2025,1,11)].drop('date',axis=1)\
        .drop_duplicates(subset='state',keep='last')\
            .tail(16).sort_values(by='reg_cumul').set_index('state')


    col_pos = sb.color_palette('Blues', n_colors=len(df)).as_hex()

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(kind='barh', width=0.7, y='reg_cumul', edgecolor='black', lw=0, color=col_pos, ax=ax)
    ax.set_title(f"""PADU: Registrations by State
    Total: {df.reg_cumul.sum():,.0f}""",linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.tick_params(axis='y',length=0)
    ax.get_legend().remove()
    ax.get_xaxis().set_visible(False)
    plt.xticks(rotation=0)
    for c in ax.containers:
        labels = [f'  {df["reg_cumul"].iloc[i]:0,.0f}' for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=10)

    print('A bar chart showing registrations for PADU by state in descending order.\n\nData:')
    for i in range(len(df)): print(f'{i+1}) {df.index[len(df)-i-1]}: {df["reg_cumul"].iloc[len(df)-1-i]:,.0f}')

    plt.savefig('padu_3_bar_abs.webp',dpi=400)
    plt.close()


def bar_rate():
    pf = pd.read_parquet('https://storage.dosm.gov.my/population/population_state.parquet') # read from OpenDOSM
    pf = pf[pf.date == pf.date.max()].drop('date',axis=1)
    pf = pf[pf.sex == 'both'].drop('sex',axis=1)
    pf.loc[pf.age == '15-19','population'] = pf.population * 0.4
    pf = pf[~pf.age.isin(['overall','0-4','5-9','10-14'])].drop('age',axis=1)
    pf = pf[~pf.ethnicity.isin(['overall','other_noncitizen'])].drop('ethnicity',axis=1)
    pf = pf.groupby('state').sum()
    pf.population = (pf.population * 1e3).astype(int)

    df = pd.read_parquet('padu.parquet',columns=['state','date','reg_cumul'])
    df = df[df.date == df.date.max()].drop('date',axis=1)\
        .drop_duplicates(subset='state',keep='last')\
            .tail(16).sort_values(by='reg_cumul').set_index('state')
    df = df.join(pf)
    df['reg_rate'] = df.reg_cumul/df.population*100
    df = df.sort_values(by='reg_rate')
    rate_msia = df.reg_cumul.sum()/df.population.sum()*100

    col_pos = sb.color_palette('Greens', n_colors=len(df)).as_hex()

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(kind='barh', width=0.7, y='reg_rate', edgecolor='black', lw=0, color=col_pos, ax=ax)
    ax.set_title(f"""PADU: Registration Rate by State
    (% of Citizens aged 18+)
    Overall: {rate_msia:,.1f}%""",linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.tick_params(axis='y',length=0)
    ax.get_legend().remove()
    ax.get_xaxis().set_visible(False)
    plt.xticks(rotation=0)
    for c in ax.containers:
        labels = [f'  {df["reg_rate"].iloc[i]:0,.1f}%' for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=10)

    print('A bar chart showing registrations for PADU by state, as a % of citizens aged 18+ in descending order.\n\nData:')
    for i in range(len(df)): print(f'{i+1}) {df.index[len(df)-i-1]}: {df["reg_rate"].iloc[len(df)-1-i]:,.1f}%')

    plt.savefig('padu_4_bar_rate.webp',dpi=400)
    plt.close()


if __name__ == '__main__':
    print('')
    make_data()
    print('')
    timeseries_abs()
    print('')
    timeseries_rate()
    print('')
    bar_abs()
    print('')
    bar_rate()
    print('')