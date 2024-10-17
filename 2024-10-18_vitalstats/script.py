import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from matplotlib.ticker import FixedFormatter, FixedLocator
from matplotlib.lines import Line2D


def births_deaths():
    bf = pd.read_parquet('https://storage.dosm.gov.my/demography/birth_sex_ethnic.parquet')
    bf = bf[bf.sex == 'both'].drop(['sex','rate'],axis=1)
    bf = bf.pivot(index='date',columns='ethnicity',values='abs').reset_index()
    bf = bf[['date','bumi_malay','chinese','indian','bumi_other']].assign(type='births')

    df = pd.read_parquet('https://storage.dosm.gov.my/demography/death_sex_ethnic.parquet')
    df = df[df.sex == 'both'].drop(['sex','rate'],axis=1)
    df = df.pivot(index='date',columns='ethnicity',values='abs').reset_index()
    df = df[['date','bumi_malay','chinese','indian','bumi_other']].assign(type='deaths')
    df = pd.concat([bf,df],axis=0,ignore_index=True)
    df.date = pd.to_datetime(df.date).dt.year

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [8,9]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,2)
    ax = ax.ravel()

    var_ori = ['bumi_malay','bumi_other','chinese','indian']
    var_title = ['Malay','Other Bumi','Chinese','Indian']
    var_blim = [40e3,5e3,20e3,5e3]

    for a in range(4):
        tf = df[['date','type',var_ori[a]]].pivot(index='date',columns='type',values=var_ori[a])
        tf.plot(y='births', ax=ax[a], color='blue')
        tf.plot(y='deaths', ax=ax[a], color='red')
        DROP = (1-tf['births'].iloc[-1]/tf.births.max())*100
        PEAK = tf.sort_values(by='births').index[-1]
        ax[a].set_title(f"""\n{var_title[a]} Births and Deaths\n(births ↓ {DROP:.0f}% from peak in {PEAK})""",linespacing=1.8)
        for b in ['top','right']: ax[a].spines[b].set_visible(False)
        ax[a].get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax[a].yaxis.grid(True)
        ax[a].set_axisbelow(True)
        ax[a].set_ylabel('')
        ax[a].set_xlabel('')
        ax[a].set_ylim(var_blim[a])
        ax[a].get_legend().remove()
    plt.suptitle('Annual Births and Deaths by Ethnicity: 2000-2023\n')

    line_blue = Line2D([0], [0], label='Births',color='blue')
    line_red = Line2D([0], [0], label='Deaths',color='red')
    fig.legend(ncol=2, handles=[line_blue, line_red], bbox_to_anchor=(0.5, 0.95), loc='upper center')
    plt.savefig('births_deaths.webp',dpi=400)
    plt.close()


def fertility():
    df = pd.read_csv('fertility.csv').set_index('year')

    eth = ['bumi_malay','bumi_other','indian','chinese']
    colours = ['blue','orange','black','red']
    eth_colours = dict(zip(eth,colours))
    eth_display = {'bumi_malay':'Malay','bumi_other':'Other Bumi','indian':'Indian','chinese':'Chinese'}

    # plot
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()
    df.plot(y=eth, ax=ax, color=colours, marker='o',markersize=4)

    # plot-wide
    ax.set_title(f"""Total Fertility Rate (TFR) by Ethnicity: 2009-2023
    TFR = How many children a woman will bear on avg
    TFR < 2 --> Can't replace both parents
    TFR < 1 --> Can't replace even 1 parent""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)

    # y-axis adjustments
    ax.set_ylabel('')
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, '.2f')))
    ax.yaxis.grid(True)
    ax.set_ylim(0.5,3)
    ax.set_yticks(np.arange(0.5,3.0,0.25))
    ax.get_legend().remove()

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xlim(2008,2024)
    ax.set_xticks(np.arange(2009,2023.1,2))

    # annotations
    for c in eth:
        ax.annotate(eth_display[c],(2023,df[c].iloc[-1]*1.03),color=eth_colours[c])
    print(ax.get_title())

    # ALT-text
    for c in ['bumi_malay','bumi_other','chinese','indian']:
        print(f'{eth_display[c]}:')
        for y in range(2009,2024):
            print(f'{y}: {df[c].loc[y]}')
        print('')

    plt.savefig('fertility.webp',dpi=400)
    plt.close()


if __name__ == '__main__':
    print('')
    births_deaths()
    print('')
    fertility()
    print('')