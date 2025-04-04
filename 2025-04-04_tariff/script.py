import pandas as pd
from datetime import datetime

from matplotlib import pyplot as plt
import seaborn as sb

REPL_COUNTRY = [
    ('Taiwan, Province Of China','Taiwan'),
    ('Korea, Republic Of','South Korea'),
    ('Viet Nam','Vietnam'),
    ('Russian Federation','Russia'),
    ('United Arab Emirates','UAE'),
    ('United States','USA'),
    ('United Kingdom','UK')
]


def make_us_dataset():
    df = pd.DataFrame(columns=['date'])

    for YEAR in [2024,2025]:
        for MONTH in range(1,13):
            if YEAR == 2024 and MONTH < 2: continue
            if YEAR == 2025 and MONTH > 1: break
            tf = pd.read_parquet(f'data/trade_hs_{YEAR}-{MONTH:02d}.parquet')
            tf = tf[tf.country == 'UNITED STATES']
            tf.hs = tf.hs.astype(str).str[:8]
            if len(df) == 0:
                df = tf.assign(date=f'{YEAR}-{MONTH:02d}').copy()
            else:
                df = pd.concat([df,tf.assign(date=f'{YEAR}-{MONTH:02d}').copy()],axis=0,ignore_index=True)

    df = df[['date','country','hs','hs_desc','imports','exports','domestic_exports']]
    for c in ['imports','exports','domestic_exports']: df[c] = pd.to_numeric(df[c],errors='coerce').astype(int)
    df.to_parquet('data/trade_us.parquet',index=False,compression='brotli')


def make_bar_by_product(V_HS='hs_2d'):
    EXEMPT = pd.read_csv('dep/hs_exempt.csv',dtype={'hs':str})['hs'].tolist()

    VISUAL_HS = {
        'hs_2d': {
            '85': 'Electrical Machinery',
            '84': 'Mechanical Machinery',
            '90': 'Medical Instruments',
            '40': 'Rubber',
            '94': 'Furniture',
            '15': 'Oils & Fats',
            '39': 'Plastics',
            '72': 'Iron and Steel',
            '18': 'Cocoa',
            '76': 'Aluminium',
            '44': 'Wood',
            '61': 'Apparel & Clothing',
            '38': 'Chemicals',
            '29': 'Organic Chemicals',
            '88': 'Aircraft & Spacecraft',
            '70': 'Glassware',
            '95': 'Toys, Games & Sports',
            '74': 'Copper',
            '48': 'Paper & Paperboard'
        },
        'hs_6d': {
            '854231': 'IC Processors',
            '854290': 'IC Parts',
            '851762': 'Telecom Equipment',
            '852351': 'Solid-State Storage',
            '854143': 'Solar Panels',
            '844399': 'Printer Parts',
            '401512': 'Medical Gloves',
            '847150': 'Computer Processors',
            '847180': 'Computer Controllers',
            '852990': 'TV & Decoder Parts',
            '854239': 'IC (Other)',
            '854142': 'Solar Cells',
            '847330': 'Circuit Boards', 
            '901819': 'Diagnostic Equipment',
            '854370': 'Electric Fence Energizers',
            '853710': 'Control Panels',
            '854232': 'Memory Chips',
            '901890': 'Medical Headlamps',
            '940350': 'Bedroom Furniture',
            '850440': 'Power Adapters'
        }
    }

    V = 'exports'

    df = pd.read_parquet('data/trade_us.parquet').assign(exempt='non-exempt')
    df.loc[df.hs.isin(EXEMPT),'exempt'] = 'exempt'
    df[V_HS] = df.hs.str[:int(V_HS[3])]
    df = df[[V_HS,'exempt',V]].groupby([V_HS,'exempt']).sum(numeric_only=True).sort_values(by=[V_HS,'exempt']).reset_index()
    df = df.pivot(index=V_HS,columns='exempt',values=V).fillna(0).astype(int).reset_index()
    df['total'] = df.sum(axis=1,numeric_only=True)
    df = df.sort_values(by='total',ascending=False)

    df[V_HS] = df[V_HS].map(VISUAL_HS[V_HS]).fillna('Others')
    df = df.groupby(V_HS).sum(numeric_only=True).sort_values(by='total',ascending=True)
    df = df/1e9
    df['total_perc'] = df['total']/df['total'].sum() * 100

    # Specifically to help plotting
    df = pd.concat([df[df.index == 'Others'],df[df.index != 'Others']],axis=0)
    df['non-exempt'] = df['non-exempt'].replace(0,0.000001)
    if V_HS == 'hs_6d': 
        df.loc[df.index == 'Others', 'non-exempt'] = df.loc[df.index == 'Others', 'non-exempt'] * 0.5

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    SPACE = '     '
    TITLE = '2D HS level' if V_HS == 'hs_2d' else '6D HS level'

    df.plot(kind='barh', width=0.7, y=['exempt', 'non-exempt'], stacked=True, edgecolor='black', lw=0, color=['#00008B', '#FFB6C1'], ax=ax)
    # plot-wide adjustments
    ax.set_title(f"""{SPACE}Msia: Exports to USA at {TITLE}
    {SPACE}from Feb 2024 to Jan 2025
    {SPACE}Exempt: RM{df.exempt.sum():,.1f} bil out of {df.total.sum():,.1f} bil ({(df.exempt.sum()/df.total.sum()*100):,.1f}%)""",linespacing=2,fontsize=11)
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
    ax.set_xticklabels([])

    for c in ax.containers:
        # Only label the total once, not for each segment
        if c == ax.containers[-1]:  # Only label the last (rightmost) container
            labels = [f"   {df['total'].iloc[i]:,.1f} bil ({df['total_perc'].iloc[i]:,.1f}%)" for i in range(len(df))]
            ax.bar_label(c, labels=labels, fontsize=10)

    # add legend manually
    legend_elements = [plt.Rectangle((0,0),2,2,facecolor='#00008B',label='Exempt'),
                    plt.Rectangle((0,0),2,2,facecolor='#FFB6C1',label='Non-exempt')]
    ax.legend(handles=legend_elements, loc='upper center', frameon=False, ncol=1, bbox_to_anchor=(0.95, 0.8))

    plt.savefig(f'output/export_us_{V_HS}.png',dpi=400)
    plt.close()

    print('\n\nALT text:')
    print(ax.get_title())
    for i in range(len(df)):
        print(f"{df.index[len(df)-i-1]}: {df.exempt.iloc[len(df)-i-1]:.1f} / {df.total.iloc[len(df)-i-1]:,.1f} bil exempt")
    print('')


def make_bar_surplus_deficit(V='trade_balance'):

    df = pd.DataFrame(columns=['date','country',V])

    for YEAR in [2024,2025]:
        for MONTH in range(1,13):
            if YEAR == 2024 and MONTH < 2: continue
            if YEAR == 2025 and MONTH > 1: break
            URL = f'/Users/theveshtheva/data/opendosm/mets/trade_hs_{YEAR}-{MONTH:02d}.parquet'
            tf = pd.read_parquet(URL)
            for c in ['imports','exports','domestic_exports','total']: tf[c] = pd.to_numeric(tf[c],errors='coerce')
            tf[V] = tf['exports'] - tf['imports']
            tf = tf[['country',V]].groupby('country').sum(numeric_only=True).sort_values(by=V,ascending=False).reset_index()
            
            if len(df) == 0:
                df = tf.assign(date=f'{YEAR}-{MONTH:02d}').copy()[['date','country',V]]
            else:
                df = pd.concat([df,tf.assign(date=f'{YEAR}-{MONTH:02d}').copy()[['date','country',V]]],axis=0,ignore_index=True)

    df = df[['country',V]].groupby('country').sum(numeric_only=True).sort_values(by=V,ascending=False).reset_index()
    df[V] = df[V]/1e9
    df.country = df.country.str.title()
    for r in REPL_COUNTRY: df.country = df.country.str.replace(r[0],r[1])
    df = df.sort_values(by=V).set_index('country')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,9]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    N = 30
    df = pd.concat([df.head(N//2),df.tail(N//2)],axis=0)
    col_pos = sb.color_palette('RdYlGn', n_colors=N).as_hex()
    df.tail(N).plot(kind='barh', width=0.7, y=V, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    SPACE = '     '
    ax.set_title(f"{SPACE}Msia: Top 15 Trade Surpluses and Deficits\n{SPACE}Feb 2024 to Jan 2025 (in RM billions)",linespacing=1.8,fontsize=11)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    plt.yticks(rotation=0, va='center')

    # y-axis adjustments
    ax.set_ylabel('')
    ax.yaxis.grid(True,alpha=0.2)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.set_xlim(-180)
    ax.set_xticklabels([])

    # annotations
    for c in ax.containers:
        labels = [f"  {df[V].iloc[i]:,.1f} bil  " for i in range(-N,0)]
        ax.bar_label(c, labels=labels,fontsize=10)

    print('\nALT text:')
    print("Top 15 Trade Deficits:")
    for i in range(N//2):
        print(f"{i+1}) {df.index[i]}: {df[V].iloc[i]:,.1f} bil")
    
    print("\nTop 15 Trade Surpluses:")
    for i in range(-1,-N//2-1,-1):
        print(f"{i*-1}) {df.index[i]}: {df[V].iloc[i]:,.1f} bil")
    print('')

    plt.savefig(f'output/trade_surplus_deficit.png',dpi=400)
    plt.close()


def make_bar_topN(V='exports',N=20):

    COLOUR = {
        'exports': 'Reds',
        'imports': 'Blues',
        'domestic_exports': 'Oranges'
    }
    TITLES = {
        'exports': 'Export Destinations',
        'imports': 'Import Origins',
        'domestic_exports': 'Export Destinations (excl. re-exports)'
    }

    df = pd.DataFrame(columns=['date','country',V])

    for YEAR in [2024,2025]:
        for MONTH in range(1,13):
            if YEAR == 2024 and MONTH < 2: continue
            if YEAR == 2025 and MONTH > 1: break
            URL = f'/Users/theveshtheva/data/opendosm/mets/trade_hs_{YEAR}-{MONTH:02d}.parquet'
            tf = pd.read_parquet(URL)
            for c in ['imports','exports','domestic_exports','total']: tf[c] = pd.to_numeric(tf[c],errors='coerce')
            tf = tf[['country',V]].groupby('country').sum(numeric_only=True).sort_values(by=V,ascending=False).reset_index()
            
            if len(df) == 0:
                df = tf.assign(date=f'{YEAR}-{MONTH:02d}').copy()[['date','country',V]]
            else:
                df = pd.concat([df,tf.assign(date=f'{YEAR}-{MONTH:02d}').copy()[['date','country',V]]],axis=0,ignore_index=True)

    df = df[['country',V]].groupby('country').sum(numeric_only=True).sort_values(by=V,ascending=False).reset_index()
    df[V] = df[V]/1e9
    df.country = df.country.str.title()
    for r in REPL_COUNTRY: df.country = df.country.str.replace(r[0],r[1])
    df[f'{V}_perc'] = df[V]/df[V].sum() * 100
    df = df.sort_values(by=f'{V}_perc').set_index('country')
    df[f'{V}_perc_cumul'] = df[f'{V}_perc'].cumsum()

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    col_pos = sb.color_palette(COLOUR[V], n_colors=N).as_hex()
    df.tail(N).plot(kind='barh', width=0.7, y=V, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    SPACE = '     '
    ax.set_title(f"{SPACE}Msia: Top {N} {TITLES[V]}\n{SPACE}Feb 2024 to Jan 2025 (in RM billions)",linespacing=1.8,fontsize=11)
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
        labels = [f"  {df[V].iloc[i]:,.1f} bil ({df[f'{V}_perc'].iloc[i]:,.1f}%)" for i in range(-N,0)]
        ax.bar_label(c, labels=labels,fontsize=10)

    # print chart title
    print('\nALT text:')
    print(ax.get_title().replace(SPACE,''))
    for i in range(-1,-N-1,-1):
        print(f"{i*-1}) {df.index[i]}: {df[V].iloc[i]:,.1f} bil  ({df[f'{V}_perc'].iloc[i]:,.1f}%)")
    print('')

    plt.savefig(f'output/top{N}_{V}.png',dpi=400)


if __name__ == '__main__':
    START = datetime.now()
    print(f'\nStart: {START:%Y-%m-%d %H:%M:%S}\n')
    print('\nGenerating bar charts by product')
    make_bar_by_product('hs_2d')
    make_bar_by_product('hs_6d')
    print('\nGenerating bar chart for surplus/deficit')
    make_bar_surplus_deficit()
    print('\nGenerating bar chart for top 20')
    make_bar_topN('exports',20)
    make_bar_topN('imports',20)
    make_bar_topN('domestic_exports',20)
    print(f'\nEnd: {datetime.now():%Y-%m-%d %H:%M:%S}\n')
    print(f'Runtime: {str(datetime.now() - START).split(".")[0]}\n')
