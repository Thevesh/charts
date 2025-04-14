import pandas as pd
import matplotlib.pyplot as plt


def make_pyramid(pf=None,CITIZEN=1):

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    GROUP = 'Citizens' if CITIZEN == 1 else 'Non-Citizen Residents'

    COLOUR_MALE = '#00008B'
    COLOUR_FEMALE = '#FFB6C1'

    # plot
    ax.barh(y=pf.index, width=pf['male'], color=COLOUR_MALE, edgecolor=COLOUR_MALE, lw=1)
    ax.barh(y=pf.index, width=pf['female'], color=COLOUR_FEMALE, edgecolor=COLOUR_FEMALE, lw=1)

    # plot-wide adjustments
    SPACE = ''
    DESC_TOTAL = f"{SPACE}Total Population: {(pf['male'].sum() * -1 + pf['female'].sum())/1e3:.1f} mil {GROUP.lower()}"
    DESC_PROP_MALE = f"{SPACE}{pf['male'].sum() * -100 / (pf['male'].sum() * -1 + pf['female'].sum()):.0f}% male"
    DESC_SEX_RATIO = f"{SPACE}Sex Ratio: {pf['male'].sum() * -100 / pf['female'].sum():.0f} males per 100 females"
    ax.set_title(f"{SPACE}Malaysia Population Pyramid (2024): {GROUP}\n{DESC_TOTAL} ({DESC_PROP_MALE})\n{DESC_SEX_RATIO}",linespacing=1.8,fontsize=11)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')
    plt.yticks(rotation=0, va='center')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)

    print(ax.get_title())
    FILENAME = 'citizen' if CITIZEN == 1 else 'noncitizen'
    plt.savefig(f'output_{FILENAME}_pyramid.png',dpi=400)


if __name__ == '__main__':

    REPL = [('0-4','00-04'),('5-9','05-09')]

    # ----- df wrangling -----
    df = pd.read_parquet('https://storage.dosm.gov.my/population/population_malaysia.parquet')
    df = df[df.date == df.date.max()]
    df = df[df.sex != 'both']
    df = df[df.age != 'overall']
    df = df[df.ethnicity != 'overall']
    df.loc[df.ethnicity != 'other_noncitizen','ethnicity'] = 'citizen'
    df.loc[df.ethnicity == 'other_noncitizen','ethnicity'] = 'non-citizen'

    for r in REPL:
        df.age = df.age.replace(r[0],r[1])
    df = df[['ethnicity','age','sex','population']].groupby(['ethnicity','age','sex'])\
        .sum()\
            .reset_index()\
                .pivot(index=['age','ethnicity'],columns='sex',values='population')\
                    .reset_index()
    for r in REPL: 
        df.age = df.age.str.replace(r[1],r[0])
    df = df.set_index('age')
    df.male = df.male * -1

    # ----- plot -----
    make_pyramid(pf=df[df.ethnicity == 'citizen'].copy(),CITIZEN=1)
    make_pyramid(pf=df[df.ethnicity == 'non-citizen'].copy(),CITIZEN=0)
