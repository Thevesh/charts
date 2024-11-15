import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def bar_chart():
    df = pd.read_csv('steps.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.loc[df.timestamp.dt.minute.isin([15,45]), 'timestamp'] -= pd.Timedelta(minutes=15)
    df = df.groupby('timestamp').sum().reset_index()


    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [8,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(kind='bar',x='timestamp',y='steps',ax=ax,color='whitesmoke',edgecolor='black', width=0.88,lw=0.3)

    # plot-wide adjustments
    ax.set_title(f"""Step Count on a Day Trip to Singapore""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('lightgrey')
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.2)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.tick_params(axis='both', which='both', colors='black', length=1, color='grey')


    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, p: f'{df.timestamp.iloc[int(x)]:%H:%M}'))

    # annotations
    ax.annotate(f'1,893 steps\nBoarding\n@ KLIA2',xy=(13.4,1700),color='red',fontsize=9,linespacing=1.5,ha='center',va='bottom')
    ax.annotate(f'548 steps\nWalking out\n@ Changi T4',xy=(14.5,600),color='red',fontsize=9,linespacing=1.5,ha='center',va='bottom')
    ax.annotate(f'1,201 steps\nMRT Expo\nto Changi T4',xy=(38.5,1000),color='red',fontsize=9,linespacing=1.5,ha='center',va='bottom')
    ax.annotate(f'435 steps\nBoarding\n@ Changi T4',xy=(44,500),color='red',fontsize=9,linespacing=1.5,ha='center',va='bottom')
    ax.annotate(f'1,872 steps\nWalking out\n@ KLIA2',xy=(43.6,1600),color='red',fontsize=9,linespacing=1.5,ha='center',va='bottom')

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df["timestamp"].iloc[i]:%H:%M}: {df["steps"].iloc[i]:,.0f}')

    plt.savefig(f'bar.webp',dpi=400)


if __name__ == '__main__':
    print('')
    bar_chart()
    print('')