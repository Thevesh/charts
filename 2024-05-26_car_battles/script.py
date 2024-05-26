import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr


def proton_v_perodua():
    df = pd.DataFrame(columns=['total','Proton','Perodua'])
    for y in range(2000,2025):
        tf = pd.read_parquet(f'https://storage.data.gov.my/transportation/cars_{y}.parquet',columns=['maker'])
        df.loc[y] = [
            len(tf),
            len(tf[tf.maker == 'PROTON']),
            len(tf[tf.maker == 'PERODUA'])
        ]

    for c in ['Proton','Perodua']: df[c] = df[c]/df['total'] * 100
    df = df.drop('total',axis=1)

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    for v,c in zip(['Perodua','Proton'],['red','black']):
        df.plot(y=v,ax=ax,color=c,marker='o',markersize=3,label=v)

    # plot-wide adjustments
    ax.set_title(f"""Perodua vs Proton: Market Share from 2000 to 2024
    (share = % of total car registrations in that year)""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True,alpha=0.5)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f')))
    ax.yaxis.set_label_coords(-0.02,1.02)
    ax.set_ylim(0)

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(True,alpha=0.5)
    plt.xticks(np.arange(2000, 2027, step=3))

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f"{df.index[i]}: {df['Proton'].iloc[i]:,.1f}% vs {df['Perodua'].iloc[i]:,.1f}%")

    plt.savefig(f'proton_v_perodua.png',dpi=400)
    plt.close()


if __name__ == '__main__':
    proton_v_perodua()
