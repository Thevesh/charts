import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import pyperclip

def turnout_comparison():
    df = pd.read_csv(f'turnout.csv').set_index('time')
    LABELS = list(df.index)

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5.5,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(y=['PRN 2023','Today'],ax=ax,color=['black','red'],marker='o',markersize=4)

    # plot-wide adjustments
    ax.set_title(f"""Voter Turnout (%) in N.06 Kuala Kubu Baharu\nPRN 2023 vs Today""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.legend(bbox_to_anchor=(0.3,0.95))

    # y-axis adjustments
    ax.set_ylim(0)
    ax.set_ylabel('')
    ax.yaxis.grid(True,alpha=0.5)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))

    # x-axis adjustments
    ax.set_xlabel('')
    plt.xticks(ticks=[x for x in range(len(LABELS))],labels=LABELS);

    # annotations
    LATEST = df.dropna(how='any').index[-1]
    N_OBS = len(df.dropna(how='any'))
    ax.annotate(f"{df.loc['18:00','PRN 2023']}%",(9,df.loc['18:00','PRN 2023']-5),color='black',fontsize=10,ha='center')
    ax.annotate(f"{df.loc[LATEST,'PRN 2023']}%",(N_OBS-1.3,df.loc[LATEST,'PRN 2023']+2),color='black',fontsize=10,ha='center')
    ax.annotate(f"{df.loc[LATEST,'Today']}%",(N_OBS-0.3,df.loc[LATEST,'Today']),color='red',fontsize=10,ha='center')

    # ALT-text copied directly to clipboard
    ALT = ''
    ALT += str(ax.get_title())
    for i in range(len(df)):
        if str(df["Today"].iloc[i]) != 'nan':
            ALT += f'\n{df.index[i]}: {df["PRN 2023"].iloc[i]}% at PRN 2023 vs {df["Today"].iloc[i]}% today'
        else:
            ALT += f'\n{df.index[i]}: {df["PRN 2023"].iloc[i]}% at PRN 2023'
    pyperclip.copy(ALT)

    plt.savefig('turnout.png',dpi=400)
    plt.close()


if __name__ == '__main__':
    turnout_comparison()
