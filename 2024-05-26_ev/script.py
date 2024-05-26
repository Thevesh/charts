import pandas as pd
import seaborn as sb
from datetime import datetime, date
from dateutil.relativedelta import relativedelta as rd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def top3(CHART_TYPE='cumulative'):
    TARGET_MAKERS = ['BYD','TESLA','BMW']

    df = pd.concat([
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2022.parquet'),
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2023.parquet'),
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2024.parquet')
    ],axis=0,ignore_index=True).rename(columns={'date_reg':'date'})
    df = df[(df.fuel == 'electric') & (df.maker.isin(TARGET_MAKERS))]
    df.date = pd.to_datetime(pd.to_datetime(df.date).dt.strftime('%Y-%m') + '-01')
    df['vehicles'] = 1
    df = df[['date','maker','vehicles']].groupby(['date','maker']).sum().reset_index()
    df = df.pivot(index='date',columns='maker',values='vehicles')
    for c in TARGET_MAKERS: df[c] = df[c].fillna(0).astype(int)
    df = df.rename(columns={'TESLA':'Tesla'})

    SDATE = datetime(2022,1,1,0,0,0)
    EDATE = df.index[-1]
    df = df[df.index >= SDATE]
    TOTALS = df.sum().to_dict()
    if CHART_TYPE == 'cumulative': df = df.cumsum()

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    for v,c in zip(['Tesla','BYD','BMW'],['black','red','blue']):
        df.plot(y=v,ax=ax,color=c,marker='o',markersize=3,label=v)

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: The EV Battle
    {CHART_TYPE.title()} Registrations with JPJ since Jan 2022
    BYD ({TOTALS['BYD']:,.0f}) vs BMW ({TOTALS['BMW']:,.0f}) vs Tesla ({TOTALS['Tesla']:,.0f})""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.5)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.yaxis.set_label_coords(-0.02,1.02)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.5)
    ax.set_xlim(SDATE-rd(months=1),EDATE+rd(months=1))

    # annotations
    for v,c in zip(['Tesla','BYD','BMW'],['black','red','blue']):
        ax.annotate(f'     {v}',(EDATE+rd(months=1), df[v].iloc[-1]*0.96),color=c,fontsize=11,ha='center')

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f"{df.index[i]:%b %Y}: {df['BYD'].iloc[i]:,.0f}, {df['BMW'].iloc[i]:,.0f}, {df['Tesla'].iloc[i]:,.0f}")

    plt.savefig(f'top3_{CHART_TYPE.lower()}',dpi=400)
    plt.close()


def bar_fueltype(START_YEAR=2022):
    df = pd.concat([
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2022.parquet'),
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2023.parquet'),
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2024.parquet')
    ],axis=0,ignore_index=True).rename(columns={'date_reg':'date'})
    df = df[df.date >= date(START_YEAR,1,1)]
    map_type = {'hybrid_petrol':'hybrid','hybrid_diesel':'hybrid','greendiesel_ng':'green diesel','petrol_ng':'petrol','other':'hybrid','greendiesel':'green diesel'}
    df.fuel = df.fuel.map(map_type).fillna(df.fuel).str.title()
    df = df.groupby('fuel').size().to_frame('vehicles').sort_values(by='vehicles')
    df['perc'] = (df.vehicles / df.vehicles.sum()) * 100

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'vehicles'
    col_pos = sb.color_palette('Greys', n_colors=len(df)).as_hex()
    df.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'Car Registrations by Fuel Type\nJan {START_YEAR} to Apr 2024',linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f"  {df[v].iloc[i]:,.0f}  ({df['perc'].iloc[i]:,.1f}%)" for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(df)):
            print(f'{i+1}) {df.index[len(df)-i-1]}: {labels[len(df)-i-1].strip()}')

    plt.savefig(f'bar_fueltype_{START_YEAR}.png',dpi=400)
    plt.close()


def bar_fueltype_top15(FUEL_TYPE='Hybrid',COLOUR='Blues'):
    df = pd.concat([
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2020.parquet'),
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2021.parquet'),
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2022.parquet'),
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2023.parquet'),
        pd.read_parquet('https://storage.data.gov.my/transportation/cars_2024.parquet')
    ],axis=0,ignore_index=True).rename(columns={'date_reg':'date'})
    map_type = {'hybrid_petrol':'hybrid','hybrid_diesel':'hybrid','greendiesel_ng':'green diesel','petrol_ng':'petrol','other':'hybrid','greendiesel':'green diesel'}
    for c in ['maker','model']: df[c] = df[c].str.title()
    df.model = df.maker + ' ' + df.model
    for r in ['Cr-V','Xc','Rx','Hr-V','Byd','Bmw','Ix','Gle','Glc']: df.model = df.model.str.replace(r,r.upper())
    df.model = df.model.str.replace('BMW I','BMW i')
    df.fuel = df.fuel.map(map_type).fillna(df.fuel).str.title()
    df = df[df.fuel == FUEL_TYPE]

    df = df.groupby('model').size().to_frame('vehicles').sort_values(by='vehicles')
    df['perc'] = (df.vehicles / df.vehicles.sum()) * 100
    df = df.tail(15)

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'vehicles'
    col_pos = sb.color_palette(COLOUR, n_colors=len(df)).as_hex()
    df.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'Top 15 {FUEL_TYPE} Car Models\nJan 2020 to Apr 2024',linespacing=1.8,fontsize=11)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f"  {df[v].iloc[i]:,.0f}  ({df['perc'].iloc[i]:,.1f}%)" for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(df)):
            print(f'{i+1}) {df.index[len(df)-i-1]}: {labels[len(df)-i-1].strip()}')

    plt.savefig(f'bar_top15_{FUEL_TYPE.lower()}.png',dpi=400)
    plt.close()


if __name__ == '__main__':
    top3(CHART_TYPE='cumulative')
    top3(CHART_TYPE='monthly')
    bar_fueltype(START_YEAR=2022)
    bar_fueltype_top15(FUEL_TYPE='Hybrid',COLOUR='Blues')
    bar_fueltype_top15(FUEL_TYPE='Electric',COLOUR='Greens')
