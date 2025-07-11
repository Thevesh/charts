# Source 1 (1901): https://www.ehm.my/publications/articles/malayas-early-20th-century-population-change
# Source 2 (1911 to 2010): https://www.ehm.my/clients/Ehm_B4CF2D68-993E-4533-A79F-522733770A7E/contentms/economic/Popu_Table_Chart_5.pdf
# Source 3 (2020 actual + 2030-2060 projections): https://open.dosm.gov.my/publications/population_projection_2060

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def timeseries_prop():
    df = pd.read_csv('data.csv').set_index('year')
    for c in df.columns: df[c] = df[c]/df['total'] * 100
    df['check'] = df.sum(axis=1)

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [8.2,8.2]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    var = ['bumi','chinese','indian','other'] # df col names 
    var_title = ['Bumi','Chinese','Indian','Lain²'] # display names
    var_colour = ['blue','red','black','orange'] # plot colours
    var_lspace = [0.95,0.87,0.67,-2.5] # adjustment for line label

    for v,c in zip(var,var_colour): df.plot(y=v,ax=ax,color=c,marker='.')

    # plot-wide adjustments
    ax.set_title(f"""Ethnic Composition of Peninsular Malaysia\nfrom 1901 to 2060 (as % of total)\n2030-2060 data are official DOSM projections""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('#cccccc')
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: f"{format(x, '.0f')}%"))
    ax.set_ylim(-4,82)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xticks(np.array(df.index.tolist()))

    # annotations
    for v,t,l,c in zip(var,var_title,var_lspace,var_colour): ax.annotate(t,(2059,df[v].iloc[-1]*l),color=c)
    for v,c in zip(var,var_colour):
        for i in range(len(df)):
            VAL = df[v].iloc[i]
            GRADIENT = 0 if i == 0 else (df[v].iloc[i]-df[v].iloc[i-1])/(df.index[i]-df.index[i-1])
            VAL_ADJ = VAL+1.25 if GRADIENT < 0 else VAL+1.15
            ax.annotate(f'{VAL:.1f}',(df.index[i],VAL_ADJ),color=c,fontsize=8.8,ha='center')

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df.index[i]}: {df["bumi"].iloc[i]:.1f}% Bumi, {df["chinese"].iloc[i]:.1f}% Chin, {df["indian"].iloc[i]:.1f}% Ind, {df["other"].iloc[i]:.1f}% Lain²\n')
    
    plt.savefig('timeseries_prop.png',dpi=300)
    plt.close()


def timeseries_abs():
    df = pd.read_csv('data.csv').set_index('year').drop('total',axis=1)
    for c in df.columns: df[c] = (df[c]/1e6).round(1)

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [8.2,8.2]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    var = ['bumi','chinese','indian','other'] # df col names 
    var_title = ['Bumi','Chinese','Indian','Lain²'] # display names
    var_colour = ['blue','red','black','orange'] # plot colours
    var_lspace = [0.95,0.87,0.67,-2] # adjustment for line label

    for v,c in zip(var,var_colour): df.plot(y=v,ax=ax,color=c,marker='.')

    # plot-wide adjustments
    ax.set_title(f"""Population of Peninsular Malaysia by Ethnicity\nfrom 1901 to 2060 (in millions)\n2030-2060 data are official DOSM projections""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('#cccccc')
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: f"{format(x, '.0f')} mil"))
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xticks(np.array(df.index.tolist()))

    # annotations
    for v,t,l,c in zip(var,var_title,var_lspace,var_colour): ax.annotate(t,(2059,df[v].iloc[-1]*l),color=c)
    for v,c in zip(var,var_colour):
        for i in range(len(df)):
            if i < 6: continue
            VAL = df[v].iloc[i]
            VAL_ADJ = VAL + 0.3 if VAL < 0.5 else VAL*1.12 if VAL < 2.3 else VAL*1.065 if VAL < 10 else VAL*1.015
            HA = 'right' if v == 'bumi' else 'center'
            ax.annotate(f'{VAL:.1f}',(df.index[i],VAL_ADJ),color=c,fontsize=8.8,ha=HA)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df.index[i]}: {df["bumi"].iloc[i]:.1f} mil Bumi, {df["chinese"].iloc[i]:.1f} mil Chinese, {df["indian"].iloc[i]:.1f} mil Indian, {df["other"].iloc[i]:.1f} mil Lain\n')

    plt.savefig('timeseries_abs.png',dpi=300)
    plt.close()


if __name__ == '__main__':
    print('')
    timeseries_prop()
    print('')
    timeseries_abs()
    print('')