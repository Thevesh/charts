import pandas as pd
import pyperclip
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

def timeseries():
    df = pd.read_csv('fdi_mida.csv').set_index('year')

    tf = pd.read_excel('fdi_dosm.xlsx')
    tf.columns = ['year','block','category','country','inflow','outflow','net','status']
    tf = tf[tf.category == 'Total']
    tf = tf.groupby(['year']).sum(numeric_only=True)
    tf = tf/1000

    df = df.join(tf, how='outer').drop(2024).rename(columns={'inflow':'Realised','approved':'Approved'})

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    for v,c in zip(['Approved','Realised'],['black','red']):
        df.plot(y=v,ax=ax,color=c,marker='o',markersize=3,label=v)

    # plot-wide adjustments
    ax.set_title(f"""Malaysia: Approved vs Realised FDI Inflows (RM bil)""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.5)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.yaxis.set_label_coords(-0.02,1.02)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.5)
    ax.set_xlim(2007,2023.9)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 2))


    # special annotation
    ax.annotate(f'Realised\n(DOSM)',(2023,240),color='red',fontsize=10,ha='center')
    ax.annotate(f'Approved\n(MIDA)',(2023,200),color='black',fontsize=10,ha='center')

        # ALT-text copied directly to clipboard
    ALT = ''
    ALT += str(ax.get_title())
    for i in range(len(df)):
        if df.index[i] < 2012:
            ALT += f'\n{df.index[i]}: RM{df["Realised"].iloc[i]:.1f} bil realised'
        else:
            ALT += f'\n{df.index[i]}: RM{df["Approved"].iloc[i]:.1f} bil approved vs RM{df["Realised"].iloc[i]:.1f} bil realised'
    pyperclip.copy(ALT)

    plt.savefig('timeseries.png',dpi=400)
    plt.close()


if __name__ == '__main__':
    timeseries()