import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import seaborn as sb


def bar_malaysia():
    df = pd.read_parquet('https://storage.dosm.gov.my/hies/hies_malaysia_percentile.parquet')
    df = df[df.date == df.date.max()].drop('date',axis=1)
    df = pd.concat([
        df[(df.variable == 'minimum') & (df.percentile.isin([41,81,91,96,100]))],
        df[(df.variable == 'median') & (df.percentile.isin([100]))]
    ],axis=0,ignore_index=True).drop('variable',axis=1)
    df.percentile = ['M40','T20','T10','T5','T1','T0.5']
    df = df.set_index('percentile')


    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [4,4]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'income'
    col_pos = sb.color_palette('Purples_r', n_colors=len(df)*2).as_hex()
    df.plot(kind='bar', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'Data for Malaysia (2022)\nMinimum Household Income to Be...\n',linespacing=2,fontsize=11)
    for b in ['top','right','left']: ax.spines[b].set_visible(False)
    ax.spines['bottom'].set_color('#cacaca')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')
    ax.set_yticklabels([])

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(True)
    plt.xticks(rotation=0)

    # annotations
    for c in ax.containers:
        labels = [f'{df[v].iloc[i]/1e3:,.1f}k\n' for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=10,linespacing=0.2)

    # ALT-text
    ALT = 0
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(df)):
            print(f'{i+1}) {df.index[i]}: {labels[i].strip()}')
        
    plt.savefig('bar_msia.png',dpi=400)
    plt.close()


def bar_state():
    df = pd.read_parquet('https://storage.dosm.gov.my/hies/hies_state_percentile.parquet')
    df = df[df.date == df.date.max()].drop('date',axis=1)
    df = pd.concat([
        df[(df.variable == 'minimum') & (df.percentile.isin([41,81,91,96,100]))],
        df[(df.variable == 'median') & (df.percentile.isin([100]))]
    ],axis=0,ignore_index=True).drop('variable',axis=1)
    df = df.sort_values(by=['state','percentile'])
    df.percentile = ['M40','T20','T10','T5','T1','T0.5']*16

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [14,14]
    plt.rcParams["figure.autolayout"] = True
    fig, axes = plt.subplots(4,4,sharex=False,sharey=False)
    ax = axes.ravel()

    sf = df.drop_duplicates(subset=['state'],keep='last').sort_values(by='income',ascending=False)

    i = 0
    for s in sf['state'].tolist():
        v = 'income'
        tf = df[df.state == s].copy().set_index('percentile')
        col_pos = sb.color_palette('Blues_r', n_colors=len(tf)+7).as_hex()
        tf.plot(kind='bar', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax[i])

        # plot-wide adjustments
        ax[i].set_title(f'\n{s}',linespacing=2,fontsize=11)
        for b in ['top','right','left']: ax[i].spines[b].set_visible(False)
        ax[i].spines['bottom'].set_color('#cacaca')
        ax[i].get_legend().remove()
        ax[i].set_axisbelow(True)
        ax[i].tick_params(axis=u'both', which=u'both',length=0,rotation=0)

        # y-ax[i]is adjustments
        ax[i].set_ylabel('')
        ax[i].set_yticklabels([])

        # x-ax[i]is adjustments
        ax[i].set_xlabel('')
        ax[i].xaxis.grid(False)
        ax[i].get_xaxis().set_visible(True)

        # annotations
        for c in ax[i].containers:
            labels = [f'{tf[v].iloc[i]/1e3:,.0f}k\n' for i in range(len(tf))]
            ax[i].bar_label(c, labels=labels,fontsize=10,linespacing=0.2)
        
        i += 1

    plt.suptitle(f'Household Income Data by State (2022)\nMinimum Household Income to Be...',linespacing=2,fontsize=12)
    plt.savefig('bar_state.png',dpi=400)
    plt.close()


def scatter_state():
    TARGET = ['M40','T20','T10','T5','T1','T0.5']
    TARGET_PLOT = ['M40','T20','T10','T1']
    PLOT_COLOURS = ['black','#8d99ae','blue','red']
    COLOURS = dict(zip(TARGET_PLOT,PLOT_COLOURS))

    df = pd.read_parquet('https://storage.dosm.gov.my/hies/hies_state_percentile.parquet')
    df = df[df.date == df.date.max()].drop('date',axis=1)
    df = pd.concat([
        df[(df.variable == 'minimum') & (df.percentile.isin([41,81,91,96,100]))],
        df[(df.variable == 'median') & (df.percentile.isin([100]))]
    ],axis=0,ignore_index=True).drop('variable',axis=1)
    df = df.sort_values(by=['state','percentile'])
    df.percentile = TARGET*16
    df = df.pivot(index='state',columns='percentile',values='income')[TARGET_PLOT].sort_values(by='M40')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6.5,6.5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'income'
    for t in TARGET_PLOT: 
        ax.scatter(df[t], df.index, color=COLOURS[t], marker='o', s=50, label=t)

    # plot-wide adjustments
    ax.set_title(f'Household Income by State and Percentile\n\n',linespacing=2,fontsize=11)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['bottom','left']: ax.spines[b].set_color('#cacaca')
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')
    ax.yaxis.grid(True)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xlim(0)
    ax.xaxis.grid(True)
    ax.get_xaxis().set_visible(True)
    plt.xticks(rotation=0)
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    # legend
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [x for x in range(len(TARGET_PLOT))]
    ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order], labelspacing=1, 
            loc='upper center', framealpha=0.7, ncols=5, bbox_to_anchor=(0.5, 1.1))

    # ALT text
    for s in df.index:
        print(f"{s}: {df.loc[s,'M40']/1000:,.1f}k, {df.loc[s,'T20']/1000:,.1f}k, {df.loc[s,'T10']/1000:,.1f}k, {df.loc[s,'T1']/1000:,.1f}k")

    plt.savefig('scatter_state.png',dpi=400)
    plt.close()


if __name__ == '__main__':
    bar_malaysia()
    bar_state()
    scatter_state()
