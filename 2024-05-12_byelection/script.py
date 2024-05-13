import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import pyperclip

def byelections():
    df = pd.read_csv('byelections.csv').set_index('election')
    df.index = df.index.str.replace('[','(').str.replace(']',')')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'Monospace',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [7,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    # plot
    df.plot(kind='barh', width=0.7, y=['turnout'], lw=0, color='#C0C0C0', alpha=0.6, ax=ax, label=['By-Election'])
    ax.scatter(df['benchmark'], df.index, color='#c40001', marker='o', s=30, label='PRU/PRN')  # Add this line for the red X
    ax.set_title(f'By-Election Voter Turnout\nvs most recent PRU/PRN\n\n',linespacing=1.8)

    # plot-wide adjustments
    for d in ['x','y']: 
        ax.tick_params(axis=d, length=0)
    for d in ['top','right','bottom']: ax.spines[d].set_visible(False)
    ax.set_axisbelow(True)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_xticklabels([])

    # custom legend
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1,0]
    ax.legend(
        [handles[i] for i in order],
        [labels[i] for i in order], 
        labelspacing=1, framealpha=0.7, ncols=len(order), 
        loc='upper center', bbox_to_anchor=(0.5, 1.08)
    )

    # annotations
    for t, b, y in zip(df['turnout'], df['benchmark'], df.index):
        offset = 18 if b > t else -18
        ax.annotate(f'{b:.0f}%', (b, y), textcoords="offset points", xytext=(offset,-3), ha='center', fontsize=10, color='#c40001')
        ax.annotate(f'{t:.0f}%', (t, y), textcoords="offset points", xytext=(0,-3), ha='center', fontsize=10.2, color='black')

    # ALT-text - copied directly to clipboard
    ALT = ''
    ALT += str(ax.get_title())
    for i in range(len(df)):
        ALT += f'\n{df.index[i]}: {df["turnout"].iloc[i]}% during by-election vs {df["benchmark"].iloc[i]}% at PRU/PRN\n'
    pyperclip.copy(ALT)

    plt.savefig('turnout.png',dpi=400)
    plt.close()


if __name__ == '__main__':
    byelections()
