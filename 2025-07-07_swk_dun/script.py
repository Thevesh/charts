import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as tkr


def bar_dun_distribution():
    state_short = {
        'Perlis': 'PLS',
        'Kedah': 'KDH',
        'Kelantan': 'KEL',
        'Terengganu': 'TRG',
        'Pulau Pinang': 'PP',
        'Perak': 'PRK',
        'Pahang': 'PHG',
        'Selangor': 'SGR',
        'Negeri Sembilan': 'N9',
        'Melaka': 'MLK',
        'Johor': 'JHR',
        'Sabah': 'SBH',
        'Sarawak': 'SWK',
    }

    df = pd.read_csv('voters_ge15.csv')[['state','dun','total']]
    df = df[~df.state.str.contains('W.P.')].reset_index(drop=True)
    df['colour'] = '#c3c3c3'
    df.loc[df.state == 'Sarawak','colour'] = '#d7292f'
    df.loc[df.state == 'Sabah','colour'] = '#6ecefa'
    # df = df.sort_values(by='total', ascending=False)

    lf = df.copy().reset_index().rename(columns={'index':'idx'})[['state','idx']]
    lf['line'] = lf.groupby('state')['idx'].transform('min')
    lf['middle'] = lf.groupby('state')['idx'].transform('mean')
    lf = lf[['state','line','middle']].drop_duplicates()
    lf['state_short'] = lf.state.map(state_short)

    plt.rcParams.update({'font.size': 11,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [10,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    # for p in selected_parties: ax.axhline(y=n_voters["voters"][p], linestyle='--', color=party_color[p])
    df.plot(kind='bar', width=1, y='total', edgecolor='black', lw=0, color=df.colour.tolist(), ax=ax)
    ax.set_title(f'DUN Seat Sizes by State (as of GE15 in 2022)\n')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.set_ylabel('')
    ax.tick_params(axis=u'both', which=u'both',length=0)
    ax.axes.get_xaxis().set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # plot a vertical line at the middle of each state
    for i in range(len(lf)):
        if i > 0: 
            ax.axvline(x=lf.line.iloc[i], color='black', alpha=0.5, linestyle='--', linewidth=0.5)
        ax.text(lf.middle.iloc[i], 120000, lf.state_short.iloc[i], ha='center', fontsize=10)

    plt.savefig('dun_distribution.png', dpi=400, bbox_inches='tight')


def bar_dun_size(V='maxmin'):
    df = pd.read_csv('voters_ge15.csv')[['state','dun','total']]
    df = df[~df.state.str.contains('W.P.')]

    pf = df.groupby('state').agg({'total': 'sum'}).reset_index()
    pf['seats'] = df.groupby('state').agg({'total': 'size'}).reset_index()['total']
    pf['avg'] = pf['total'] / pf['seats']
    pf['min'] = df.groupby('state').agg({'total': 'min'}).reset_index()['total']
    pf['max'] = df.groupby('state').agg({'total': 'max'}).reset_index()['total']
    pf['maxmin'] = pf['max']/pf['min']
    pf['std'] = df.groupby('state').agg({'total': 'std'}).reset_index()['total']
    pf = pf.sort_values(by='maxmin', ascending=True).set_index('state')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    colour = 'Reds' if V == 'maxmin' else 'Blues'
    col_pos = sb.color_palette(colour, n_colors=len(pf)).as_hex()
    pf.plot(kind='barh', width=0.7, y=V, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    SPACE = ''
    var_desc = 'Size of biggest DUN vs smallest DUN' if V == 'maxmin' else 'Voters per DUN (assuming Swk = 99)'
    ax.set_title(f"{SPACE}DUN Seats by State\n{var_desc}\n(as of GE15 in 2022)",linespacing=1.8,fontsize=11)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')
    plt.yticks(rotation=0, va='center')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f"  {pf[V].iloc[i]:,.2f}x" for i in range(len(pf))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # print chart title
    print('\nALT text:')
    print(ax.get_title().replace(SPACE,''))
    for i in range(len(pf)):
        print(f"{i+1}) {pf.index[-i-1]}: {pf[V].iloc[-i-1]:,.2f}x")
    print('')

    plt.savefig(f'dun_ge15_{V}.png', dpi=400, bbox_inches='tight')
    pf.total = (pf.total/1e6).round(1)
    pf.sort_values(by='seats')


if __name__ == '__main__':
    bar_dun_distribution()
    bar_dun_size(V='maxmin')
    bar_dun_size(V='avg')