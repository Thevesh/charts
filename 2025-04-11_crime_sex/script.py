import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sb


def make_bar_cases_capita(df=None,V='rate',AGE='all'):
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed',
                        'font.weight': 'light'})

    plt.rcParams["figure.figsize"] = [5*2,5*2]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,2)
    ax = ax.ravel()

    VARS = ['rape','incest','molest','sexual_harassment']
    TITLES = ['Rape','Incest','Molestation','Sexual Harassment']

    col_pos = sb.color_palette('Reds', n_colors=len(df.state.unique())).as_hex()

    for i in range(len(VARS)):
        pf = df[(df.date == df.date.max()) & (df.age == AGE)].copy()
        pf['rate'] = pf[VARS[i]] / pf['population'] * 100
        pf = pf.sort_values(by='rate',ascending=True).set_index('state')
        pf.plot(kind='barh', width=0.7, y=V, edgecolor='black', lw=0, color=col_pos, ax=ax[i])

        # plot-wide adjustments
        ax[i].set_title(f'\n{TITLES[i]}',linespacing=0.5)
        for b in ['top','right','bottom']: ax[i].spines[b].set_visible(False)
        ax[i].spines['left'].set_color('#c9c9c9')
        ax[i].get_legend().remove()
        ax[i].set_axisbelow(True)
        ax[i].tick_params(axis=u'both', which=u'both',length=0)

        # y-axis adjustments
        ax[i].set_ylabel('')

        # x-axis adjustments
        ax[i].set_xlabel('')
        ax[i].xaxis.grid(False)
        ax[i].get_xaxis().set_visible(False)
        for c in ax[i].containers:
            labels = [f'  {pf[V].iloc[i]:,.2f}' for i in range(len(pf))]
            ax[i].bar_label(c, labels=labels,fontsize=10)

        # ALT-text
        ALT = 1
        if ALT == 1:
            print(ax[i].get_title().strip())
            for i in range(len(pf)):
                print(f'{i+1}) {pf.index[len(pf)-i-1]}: {labels[len(pf)-i-1].strip()}')

    VICTIM = 'Victims of All Ages' if AGE == 'all' else 'Victims below 18yo'
    plt.suptitle(f'Sexual Crime Cases per 100k Population\nData for 2023, involving {VICTIM}',linespacing=1.8)
    plt.savefig(f'cases_{AGE}.png',dpi=400)
    plt.close()


def make_bar_cases_prop_child(rf=None,V='prop'):
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed',
                        'font.weight': 'light'})

    plt.rcParams["figure.figsize"] = [5*2,5*2]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,2,sharex=True)
    ax = ax.ravel()

    V = 'prop'
    VARS = ['rape','incest','molest','sexual_harassment']
    TITLES = ['Rape','Incest','Molestation','Sexual Harassment']

    col_pos = sb.color_palette('Oranges', n_colors=len(rf.state.unique())).as_hex()

    for i in range(len(VARS)):
        pf = rf[rf.crime == VARS[i]]
        pf = pf.sort_values(by=V,ascending=True).set_index('state')
        pf.plot(kind='barh', width=0.7, y=V, edgecolor='black', lw=0, color=col_pos, ax=ax[i])

        # plot-wide adjustments
        ax[i].set_title(f'\n{TITLES[i]}',linespacing=0.5)
        for b in ['top','right','bottom']: ax[i].spines[b].set_visible(False)
        ax[i].spines['left'].set_color('#c9c9c9')
        ax[i].get_legend().remove()
        ax[i].set_axisbelow(True)
        ax[i].tick_params(axis=u'both', which=u'both',length=0)

        # y-axis adjustments
        ax[i].set_ylabel('')

        # x-axis adjustments
        ax[i].set_xlabel('')
        ax[i].xaxis.grid(False)
        ax[i].get_xaxis().set_visible(False)
        for c in ax[i].containers:
            labels = [f'  {pf[V].iloc[i]:,.2f}' for i in range(len(pf))]
            ax[i].bar_label(c, labels=labels,fontsize=10)

        # ALT-text
        ALT = 1
        if ALT == 1:
            print(ax[i].get_title().strip())
            for i in range(len(pf)):
                print(f'{i+1}) {pf.index[len(pf)-i-1]}: {labels[len(pf)-i-1].strip()}')

    plt.suptitle(f'Proportion of Sexual Crimes Involving Children\nData for 2023',linespacing=1.8)
    plt.savefig(f'cases_prop_child.png',dpi=400)
    plt.close()

if __name__ == '__main__':

    # Note on data: Manual adjustment made to values for KL and N9 for incest for 2023, otherwise child cases > total cases
    # KL adjusted from 5 to 8 (matching child cases)
    # Negeri Sembilan adjusted from 11 to 12 (matching child cases)
    # However, this does call into question the accuracy of the data

    df = pd.read_csv('data.csv').drop(['total','unnatural_sex'],axis=1).rename(columns={'year':'date'})
    df['date'] = pd.to_datetime(df['date'],format='%Y').dt.date
    df['total'] = df.sum(axis=1,numeric_only=True)
    df = df[df.state != 'Malaysia']

    pf = pd.read_parquet('https://storage.dosm.gov.my/population/population_state.parquet')
    pf = pf[pf.date.isin(df.date)]
    pf = pf[(pf.sex == 'both') & (pf.age == 'overall') & (pf.ethnicity == 'overall')][['state','date','population']]
    pf = pf.replace('W.P. Labuan','Sabah').replace('W.P. Putrajaya','W.P. Kuala Lumpur')
    pf = pf.groupby(['date','state']).sum().reset_index()

    df = pd.merge(df,pf,on=['date','state'],how='left')
    df.state = df.state.str.replace('W.P. Kuala Lumpur','KL + Putrajaya').replace('Sabah','Sabah + Labuan')

    rf = df[(df.date == df.date.max())].copy().drop(['date','population','total'],axis=1)
    rf = pd.melt(rf,id_vars=['state','age'],value_vars=['rape','incest','molest','sexual_harassment'],var_name='crime',value_name='cases')
    rf = rf.pivot(index=['state','crime'],columns='age',values='cases').reset_index()
    rf['prop'] = rf['child'] / rf['all'] * 100

    make_bar_cases_capita(df=df,AGE='all')
    make_bar_cases_capita(df=df,AGE='child')

    make_bar_cases_prop_child(rf=rf,V='prop')