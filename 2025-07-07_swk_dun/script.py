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
    pf.loc[pf.state == 'Sarawak','seats'] = 99
    pf['avg'] = pf['total'] / pf['seats']
    pf['min'] = df.groupby('state').agg({'total': 'min'}).reset_index()['total']
    pf['max'] = df.groupby('state').agg({'total': 'max'}).reset_index()['total']
    pf['maxmin'] = pf['max']/pf['min']
    pf['std'] = df.groupby('state').agg({'total': 'std'}).reset_index()['total']
    pf = pf.sort_values(by=V, ascending=True).set_index('state')

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
    var_desc = 'Biggest DUN vs smallest DUN\nas of GE15 (2022)' if V == 'maxmin' else 'Avg Voters per DUN as of GE15 (2022)\n(assuming Swk has 99 DUNs)'
    ax.set_title(f"{SPACE}{var_desc}",linespacing=1.8,fontsize=11)
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
        if V == 'maxmin':
            labels = [f"  {pf[V].iloc[i]:,.2f}x" for i in range(len(pf))]
        else:
            labels = [f"  {pf[V].iloc[i]:,.0f}" for i in range(len(pf))]
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


def scatter_dun_eq():
    df = pd.read_csv('voters_ge15.csv',usecols=['state','dun','total']).rename(columns={'total':'voters'})
    df = df[~df.state.str.contains('W.P.')].reset_index(drop=True)
    df['avg'] = df.groupby('state')['voters'].transform('mean').astype(int)
    df['diff_eq'] = df.voters/df.avg
    df['desc'] = 'Within 15% of avg'
    df.loc[df.diff_eq > 1.15,'desc'] = 'Oversized'
    df.loc[df.diff_eq < 0.85,'desc'] = 'Undersized'

    af = df.groupby('state').agg({'diff_eq': 'size'}).reset_index()
    af['undersized'] = df[df.diff_eq < 0.85].groupby('state').agg({'diff_eq': 'size'}).reset_index()['diff_eq']
    af['prop_undersized'] = af.undersized/af.diff_eq
    af['max_size'] = df.groupby('state').agg({'diff_eq': 'max'}).reset_index()['diff_eq']
    af = af.sort_values(by='max_size',ascending=True)
    STATE_PLOT = af.state.tolist()
    df['diff_eq'] = (df.diff_eq * 100).round(2)

    TARGET_PLOT = ['Undersized','Within 15% of avg','Oversized']
    PLOT_COLOURS = ['blue','#c3c3c3','red']
    COLOURS = dict(zip(TARGET_PLOT,PLOT_COLOURS))

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6.5,6.5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    for s in STATE_PLOT:
        for c in COLOURS:
            ax.scatter(
                df[(df.state == s) & (df.desc == c)]['diff_eq'], 
                [s]*len(df[(df.state == s) & (df.desc == c)]), 
                color=COLOURS[c], marker='o', s=70, label=c
            )

    # plot-wide adjustments
    ax.set_title(f'Size of DUNs relative to state average\nas of GE-15 (November 2022)\n\n',linespacing=2,fontsize=11)
    for b in ['top','right','left']: ax.spines[b].set_visible(False)
    for b in ['bottom','left']: ax.spines[b].set_color('#cacaca')
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    ax.grid(True,alpha=0.5)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xlim(20)
    ax.get_xaxis().set_visible(True)
    plt.xticks(rotation=0)
    ax.set_xticklabels(['','0.5x','State Avg','1.5x','2x','2.5x','3x'])

    # legend
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [x for x in range(len(TARGET_PLOT))]
    ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order], labelspacing=1, 
            loc='upper center', framealpha=0.7, ncols=5, bbox_to_anchor=(0.5, 1.09))
    
    plt.savefig('scatter_dun_eq.png', dpi=400, bbox_inches='tight')


def scatter_parlimen_eq():
    df = pd.read_csv('voters_ge15.csv',usecols=['state','parlimen','total']).rename(columns={'total':'voters'})
    df = df.groupby(['state','parlimen']).agg({'voters': 'sum'}).reset_index()
    df['avg'] = df.voters.mean()
    df['diff_eq'] = df.voters/df.avg * 100
    df['desc'] = 'Within 15% of avg'
    df.loc[df.diff_eq > 115,'desc'] = 'Oversized'
    df.loc[df.diff_eq < 85,'desc'] = 'Undersized'

    af = df.copy().groupby('state').agg({'diff_eq': 'size'})
    af = af.rename(columns={'diff_eq':'seats'})
    af['undersized'] = df[df.diff_eq < 85].groupby('state').agg({'diff_eq': 'size'})
    af['oversized'] = df[df.diff_eq > 115].groupby('state').agg({'diff_eq': 'size'})
    af['within'] = af.seats - af.undersized - af.oversized
    for c in ['undersized','oversized','within']:
        af[c] = af[c].fillna(0).astype(int)
        af[f'prop_{c}'] = af[c]/af.seats * 100
    af['max_size'] = df.groupby('state').agg({'diff_eq': 'max'})['diff_eq']
    af = af.sort_values(by='max_size',ascending=True)
    STATE_PLOT = af.index.tolist()

    TARGET_PLOT = ['Undersized','Within 15% of avg','Oversized']
    PLOT_COLOURS = ['blue','#c3c3c3','red']
    COLOURS = dict(zip(TARGET_PLOT,PLOT_COLOURS))

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [7,7]
    plt.rcParams["figure.autolayout"] = True
    _, ax = plt.subplots()

    for s in STATE_PLOT:
        for c in COLOURS:
            ax.scatter(
                df[(df.state == s) & (df.desc == c)]['diff_eq'], 
                [f'{s} [{len(df[(df.state == s)])}]']*len(df[(df.state == s) & (df.desc == c)]), 
                color=COLOURS[c], marker='o', s=70, label=c
            )

    # plot-wide adjustments
    ax.set_title(f'Size of Parlimens vs national average\nas of GE-15 (November 2022)\n\n',linespacing=2,fontsize=11)
    for b in ['top','right','left']: ax.spines[b].set_visible(False)
    for b in ['bottom','left']: ax.spines[b].set_color('#cacaca')
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    ax.grid(True,alpha=0.5)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xlim(0)
    ax.get_xaxis().set_visible(True)
    plt.xticks(rotation=0)
    ax.set_xticklabels(['','0.5x','National Avg','1.5x','2x','2.5x','3x'])

    # legend
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [x for x in range(len(TARGET_PLOT))]
    ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order], labelspacing=1, 
            loc='upper center', framealpha=0.7, ncols=5, bbox_to_anchor=(0.5, 1.08))

    plt.savefig('scatter_parlimen_eq.png', dpi=400, bbox_inches='tight')


if __name__ == '__main__':
    # bar_dun_distribution()
    # bar_dun_size(V='maxmin')
    # bar_dun_size(V='avg')
    # scatter_dun_eq()
    scatter_parlimen_eq()