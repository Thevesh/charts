import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

RAMADAN = pd.read_csv('dates.csv',date_format='%Y-%m-%d',parse_dates=['ramadan'])['ramadan'].tolist()
STAND_OUT = '#E63946'
BASE = '#A8DADC'


def timeseries_bar(tf = None):

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [8,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    tf[tf.date != tf.date.max()].plot(kind='bar',x='date',y='donations',ax=ax,color=list(tf.color)[:-1],edgecolor='none', width=0.88,lw=0.3)

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: Monthly Blood Donations from 2012-2025\n(Ramadan months are plotted in red)\n""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('lightgrey')
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.2)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.tick_params(axis='both', which='both', colors='black', length=1, color='grey')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True)
    ax.xaxis.set_major_locator(tkr.IndexLocator(base=12, offset=-12))
    ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, p: f'{df.date.iloc[int(x+1)]:%Y}'))

    # save and close
    for ext in ['png','webp']: plt.savefig(f'blood_donations.{ext}',dpi=300)
    print('Saved charts')
    plt.close()



if __name__ == '__main__':

    print(f'\nStart: {datetime.now()}: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

    df = pd.read_parquet('https://storage.data.gov.my/healthcare/blood_donations.parquet')
    df = df[df.blood_type == 'all'].drop('blood_type',axis=1)
    df['date'] = pd.to_datetime(df['date']).dt.to_period('M').dt.to_timestamp()
    df = df[(df.date.dt.year >= 2012) & (df.date.dt.year <= 2025)]
    df = df.groupby('date')['donations'].sum().reset_index()\
        .assign(ramadan=lambda x: x.date.isin(RAMADAN), color=lambda x: np.where(x.date.isin(RAMADAN), STAND_OUT, BASE))
    df.date = pd.to_datetime(df.date)

    timeseries_bar(tf=df)

    print(f'\nEnd: {datetime.now()}: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')