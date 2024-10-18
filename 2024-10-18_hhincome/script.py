import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import seaborn as sb

def bar_state():
    df = pd.read_parquet('https://storage.dosm.gov.my/hies/hies_state_percentile.parquet')
    df = df[df.date == df.date.max()].drop('date',axis=1)
    df = df[(df.variable == 'minimum') & (df.percentile == 86)][['state','income']].set_index('state').sort_values(by='income')


    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'income'
    col_pos = sb.color_palette('Greens', n_colors=len(df)).as_hex()
    df.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'Monthly Household Income\nrequired to be T15',linespacing=1.8)
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
        labels = [f'  {df[v].iloc[i]:,.0f}' for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(df)):
            print(f'{i+1}) {df.index[len(df)-i-1]}: {labels[len(df)-i-1].strip()}')
    
    plt.savefig('bar_state.webp',dpi=400)
    plt.close()


def scatter_state():
    TARGET = ['M40','T20','T15','T10','T5','T1','T0.5']
    TARGET_PLOT = ['M40','T20','T15','T10','T1']
    PLOT_COLOURS = ['black','#8d99ae','red','orange','blue']
    COLOURS = dict(zip(TARGET_PLOT,PLOT_COLOURS))

    df = pd.read_parquet('https://storage.dosm.gov.my/hies/hies_state_percentile.parquet')
    df = df[df.date == df.date.max()].drop('date',axis=1)
    df = pd.concat([
        df[(df.variable == 'minimum') & (df.percentile.isin([41,81,86,91,96,100]))],
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
    ALT = 1
    if ALT == 1:
        for s in df.index:
            print(f"{s}: {df.loc[s,'M40']/1000:,.1f}k, {df.loc[s,'T20']/1000:,.1f}k, {df.loc[s,'T15']/1000:,.1f}k, {df.loc[s,'T10']/1000:,.1f}k, {df.loc[s,'T1']/1000:,.1f}k")

    plt.savefig('scatter_state.webp',dpi=400)
    plt.close()


if __name__ == '__main__':
    print('')
    bar_state()
    print('')
    scatter_state()
    print('')

