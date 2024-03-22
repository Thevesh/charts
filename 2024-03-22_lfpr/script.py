import os

import pandas as pd
from datetime import date, datetime

import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def heatmap():
    df = pd.read_excel('lfpr.xlsx',sheet_name='sex')
    df.state = df.state + ' '
    df = df[~df.state.str.contains('Malaysia')].set_index('state').sort_values(by='overall',ascending=False)
    df[''] = np.nan
    df = df[[
        'male','female','',
        'male_urban','female_urban','',
        'male_rural','female_rural'
    ]]
    df.columns = ['Male (M)','Female (F)','','Urban (M)','Urban (F)','','Rural (M)','Rural (F)']

    # sb.set(font="Monospace")
    fig, ax = plt.subplots(figsize=[8, 7])  # width, height

    # heatmap
    sb.heatmap(df,
            annot=True, fmt=",.1f",
            annot_kws={'fontsize': 9},
            cmap='Blues',
            cbar=False,
            cbar_kws={"shrink": .9}, ax=ax)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_facecolor('white')
    ax.set_title('Labour Force Participation Rate (2022)\nby State, Strata and Sex (%)\n', fontsize=10.5, linespacing=1.8)

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
        for i in range(len(df)): print(f'{df.index[i]}: {df["Male (M)"].iloc[i]:.1f}% for male, {df["Female (F)"].iloc[i]:.1f}% for female')
        
    plt.savefig(f'heatmap.png',dpi=400, bbox_inches = 'tight')
    plt.close()


CURDIR = os.getcwd()
os.chdir(f'{CURDIR}/2024-03-22_lfpr/')

print('')
heatmap()
print('')

os.chdir(CURDIR)
