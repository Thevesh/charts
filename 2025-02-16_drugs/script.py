import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
import seaborn as sb


def heatmap_state():
    pf = pd.read_parquet('https://storage.dosm.gov.my/population/population_state.parquet')
    pf.date = pd.to_datetime(pf.date).dt.year
    pf = pf[pf.age == 'overall'].drop('age',axis=1)
    pf = pf[~pf.ethnicity.isin(['other_noncitizen','overall'])]
    pf = pf[pf.date >= 2018]

    df = pd.melt(pd.read_csv('state.csv'),id_vars=['state'],value_vars=[str(x) for x in range(2018,2025)],var_name='date',value_name='cases')
    df.date = df.date.astype(int)

    tfp = pf[(pf.sex == 'both')].groupby(['date','state']).sum(numeric_only=True).reset_index()
    df = pd.merge(df,tfp,on=['date','state'],how='left')
    df['cases_100k'] = df['cases']/df['population'] * 100 # pop already in 1000s
    df = df.pivot(index=['state'],columns='date',values='cases_100k').round(0).astype(int)
    df[' '] = np.nan
    df['7y avg'] = df.iloc[:,1:-1].mean(axis=1).round(0).astype(int)
    df = df.sort_values(by='7y avg',ascending=False)

    fig, ax = plt.subplots(figsize=[7, 7])  # width, height

    # heatmap
    sb.heatmap(df,
            annot=True, fmt=",.0f",
            annot_kws={'fontsize': 9},
            cmap='Reds',
            cbar=False,
            cbar_kws={"shrink": .9}, ax=ax)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_facecolor('white')
    ax.set_title('Drug Cases per 100k Citizens by State\n', fontsize=10.5, linespacing=1)

    # ticks
    plt.yticks(rotation=0)
    ax.tick_params(axis=u'both', which=u'both',
                length=0, labelsize=10, 
                labelbottom=False, labeltop=True,
                bottom=False, top=False)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)):
            print(f'{df.index[i]}: {df["7y avg"].iloc[i]:.0f}')

    plt.savefig(f'heatmap_state.png',dpi=400, bbox_inches = 'tight')
    plt.savefig(f'heatmap_state.webp',dpi=400, bbox_inches = 'tight')
    plt.close()


if __name__ == '__main__':
    print(f'\nStart: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print('\nGenerating state heatmap')
    heatmap_state()
    print(f'\nDone: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')