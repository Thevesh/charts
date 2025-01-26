import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from matplotlib.lines import Line2D
from datetime import datetime


def timeseries():
    VAR = ['cny','deepavali'] + [f'raya{x}' for x in range(1,6)]

    df = pd.read_csv('data.csv').set_index('year')
    for v in VAR:
        df[v] = pd.to_datetime(df[v], errors='coerce')
        df[v] = df[v].apply(
            lambda x: ((x - pd.Timestamp(f"{x.year}-01-01")).days // 7 + 1) if pd.notnull(x) else None
        )

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [8,8]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()


    COLOUR = ['red','#FFD700'] + ['blue'] * 5

    for v,c in zip(VAR,COLOUR): df[v].plot(y=v,ax=ax,color=c,lw=1.2)

    # plot-wide adjustments
    ax.set_title("""Hari Raya Aidilfitri, CNY, and Deepavali Dates (1957 - 2077)\n
    Kongsi Raya: 1965-66, 1996-98, 2029-31, 2062-63\n
    DeepaRaya: 1972-73, 2004-06, 2037-38, 2070-72\n
    \n""",linespacing=1)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('#cccccc')
    ax.set_axisbelow(True)

    # y-axis adjustments
    ax.set_ylabel('Week\nof Year',linespacing=1.2,rotation=0,ha='center')
    ax.yaxis.set_label_coords(-0.02,1.01)
    ax.yaxis.grid(True,alpha=0.3)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.set_ylim(0,52)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.3)
    ax.set_xlim(1955,2085)

    # Lines + annotations for Raya 2x per year
    for y in [1968,2000,2033,2065]:
        MAP_YMIN = {1968:0.02, 2000:0.04,  2033:0.02, 2065:0.04}
        MAP_YMAX = {1968:0.98, 2000:0.994, 2033:0.98, 2065:0.994}
        ax.axvline(x=y, color='blue', ymin=MAP_YMIN[y], ymax=MAP_YMAX[y], lw=1)

        ax.annotate(f'{y}:\nRaya 2x', xy=(y-1, 26), xytext=(y-1, 26),
                    color='blue',fontsize=10,va='center',ha='right')
        
    # circles for Kongsi Raya and Deeparaya
    for y in [1973,2005,2038,2070]: ax.plot(y,44, 'o', color='black', markersize=20, mew=1.5, fillstyle='none')
    for y in [1965,1998,2030,2063]: ax.plot(y,5, 'o', color='black', markersize=20, mew=1.5, fillstyle='none')

    # custom legend
    raya = Line2D([0], [0], label='Hari Raya',color='blue')
    cny = Line2D([0], [0], label='CNY',color='red')
    deepavali = Line2D([0], [0], label='Deepavali',color='gold')
    fig.legend(ncol=3, handles=[raya, cny, deepavali], bbox_to_anchor=(0.5, 0.845), loc='upper center')

    plt.savefig('timeseries.webp',dpi=400)
    plt.close()


if __name__ == '__main__':
    print(f'\nStart: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print('\nGenerating timeseries')
    timeseries()
    print(f'\nDone: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
