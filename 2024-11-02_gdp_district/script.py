import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from matplotlib.ticker import StrMethodFormatter

def scatter(VAR_PLOT='value'):

    cf = pd.read_excel('gdp_capita.xlsx')
    cf.district = cf.district.str.strip().replace('Larut dan Matang','Larut Dan Matang')
    cf = cf[['district',2019]].rename(columns={2019:'capita'})

    df = pd.read_parquet('https://storage.dosm.gov.my/gdp/gdp_district_real_supply.parquet')
    df = df[df['series'] == 'abs'].drop('series',axis=1)
    df = df[df.sector == 'p0'].drop('sector',axis=1)
    df = df[df.date == date(2019,1,1)].drop('date',axis=1)
    df = df[~df.state.str.contains('W.P.')]
    df = df[~df.district.str.contains('Supra')]
    df['value'] = df['value'] / 1000
    df = pd.merge(df,cf,on='district',how='left')
    df = df.sort_values(by=VAR_PLOT,ascending=False)

    PLOT = df.copy().drop_duplicates(subset='state')['state'].tolist()[::-1]
    df = df.set_index('state')


    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6.5,6.5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    for p in PLOT:
        ax.scatter(df[df.index == p][VAR_PLOT], df[df.index == p].index, color='black', marker='o', s=30)

    # plot-wide adjustments
    TITLE = f'GDP per Capita by District' if VAR_PLOT == 'capita' else 'GDP by District in RM billions'
    ax.set_title(f'{TITLE} (2019)\n(note: 2020 not used to avoid pandemic distortion)',linespacing=2,fontsize=11)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['bottom','left']: ax.spines[b].set_color('#cacaca')
    for b in ['left']: ax.spines[b].set_color('white')
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')
    ax.yaxis.grid(True, alpha=0.3)

    # x-axis adjustments
    ax.set_xlabel('')
    if VAR_PLOT == 'value':
        ax.set_xlim(-4.9,201)
    ax.xaxis.grid(True, alpha=0.3)
    ax.get_xaxis().set_visible(True)
    plt.xticks(rotation=0)
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    for p in PLOT:
        state_districts = df[df.index == p]
        top_district = state_districts.sort_values(by=VAR_PLOT, ascending=False).iloc[0]
        ax.annotate(f'  {top_district.district}', 
                    xy=(top_district[VAR_PLOT], p),
                    xytext=(5, 0), 
                    textcoords='offset points',
                    va='center',
                    fontsize=9,c='red')

    FILENAME = '_capita' if VAR_PLOT == 'capita' else '_value'
    plt.savefig(f'scatter{FILENAME}.webp',dpi=400)

    # ALT text
    ALT = 1
    if ALT == 1:
        filename = 'alt_capita.txt' if VAR_PLOT == 'capita' else 'alt_value.txt'
        with open(filename, 'w') as f:
            f.write(ax.get_title().strip() + '\n')
            for p in PLOT:
                f.write(f'\nData for {p}:\n')
                state_districts = df[df.index == p].sort_values(by=VAR_PLOT, ascending=False)
                for _, district in state_districts.iterrows():
                    f.write(f"{district.district}: {district[VAR_PLOT]:,.1f}\n")


if __name__ == '__main__':
    print('')
    scatter(VAR_PLOT='capita')
    print('')
    scatter(VAR_PLOT='value')
    print('')