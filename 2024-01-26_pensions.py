import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

PATH = '2024-01-26_pensions'


def timeseries_pension_politician():
    df = pd.read_excel(f'src/{PATH}.xlsx').set_index('year')

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [7,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(y='politician',ax=ax,color='red',marker='.')

    # plot-wide adjustments
    ax.set_title(f"""Jumlah Peruntukan bagi tujuan Pencen Ahli Politik (RM mil)\nRujukan: Dokumen Tanggungan 14 (T.14)""",linespacing=1.8)
    for b in ['top','right']: ax.spines[b].set_visible(False)
    ax.set_axisbelow(True)
    ax.get_legend().remove()

    # y-axis adjustments
    ax.yaxis.grid(True)
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, '.0f')))
    ax.set_ylim(0)
    ax.set_ylabel('RM mil',rotation='horizontal')
    ax.yaxis.set_label_coords(-0.02,1.02)

    # x-axis adjustments
    ax.set_xlabel('')
    # ax.set_xticks(np.array(df.index.tolist()))

    # annotations
    for v,c in zip(['politician'],['red']):
        for i in range(len(df)):
            VAL = df[v].iloc[i]
            GRADIENT = 0 if i == 0 else (df[v].iloc[i]-df[v].iloc[i-1])/(df.index[i]-df.index[i-1])
            VAL_ADJ = VAL-3 if GRADIENT < 0 else VAL+2
            ax.annotate(f'{VAL:.1f}',(df.index[i],VAL_ADJ),color=c,fontsize=8.8,ha='center')

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title())
        for i in range(len(df)): print(f'{df.index[i]}: RM{df["politician"].iloc[i]:.1f} mil')

    plt.savefig(f'output/{PATH}/timeseries_pension_politician.png',dpi=400)
    plt.close()


def bar_pension_politician():
    df = pd.read_excel(f'src/{PATH}.xlsx')
    df = df[df.year == 2024].drop('year',axis=1) / 1000
    df = df.transpose().drop('hakim').rename(columns={14:'jumlah'})
    df.index = ['Keseluruhan','Mengurus (OE)','Emolumen','Pencen','Pencen\nAhli Politik']

    col_pos = sb.color_palette('Reds', n_colors=len(df)).as_hex()

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'jumlah'
    df = df.sort_values(by=v,ascending=True)
    df.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'          Peruntukan mengikut Jenis Perbelanjaan (2024)\n',linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.get_legend().remove()
    ax.set_axisbelow(True)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f'  RM{df[v].iloc[i]:.1f} bil  ({df[v].iloc[i]/df.loc["Keseluruhan"].sum()*100:.2f}%)' for i in range(len(df))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(df)):
            print(f'{df.index[i]}: {labels[i].strip()}')

    plt.savefig(f'output/{PATH}/bar_pension_politician.png',dpi=400)
    plt.close()


def bar_pension():
    df = pd.read_excel(f'src/{PATH}.xlsx',sheet_name='pensions')
    df = df[df.year == 2024].drop('year',axis=1).transpose().rename(columns={14:'jumlah'})
    df.index = ['Keseluruhan','Pesara Sem Msia','Pesara Sarawak','Pesara Sabah','Polis','Tentera','Askar Johor','Rancangan BAY','Ahli Sukarela','Ahli Politik','Hakim']
    df = df/1000

    col_pos = sb.color_palette('Reds', n_colors=len(df)).as_hex()

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6,6]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'jumlah'
    df = df.sort_values(by=v,ascending=True)
    df.iloc[:-1,:].plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'Perbelanjaan Pencen 2024 mengikut Penerima\nJumlah Besar: RM{df.iloc[:-1][v].sum():.1f} bil',linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.get_legend().remove()
    ax.set_axisbelow(True)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f'  RM{df[v].iloc[i]:.3f} bil  ({df[v].iloc[i]/df.loc["Keseluruhan"].sum()*100:.2f}%)' for i in range(len(df))]
        ax.bar_label(c, labels=labels[:-1],fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(df)):
            print(f'{df.index[i]}: {labels[i].strip()}')

    plt.savefig(f'output/{PATH}/bar_pension.png',dpi=400)
    plt.close()


def timeseries_pension():
    df = pd.read_excel(f'src/{PATH}.xlsx').set_index('year')
    df = df/1000
    df['pension_prop'] = df.pension / df.oe * 100

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6.5,10]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(2,1)
    ax = ax.ravel()

    TITLE = "Jumlah Peruntukan bagi tujuan Pencen\nRujukan: Lampiran C, Objek Sebagai 46000\n"
    plt.suptitle(TITLE,linespacing=1.8)

    vars = ['pension','pension_prop']
    titles = ["Jumlah Mutlak (RM bil)","\nNisbah kepada Perbelanjaan Mengurus (%)"]
    yaxes = ['RM bil','% drpd OE']
    ylims = [29,11]

    for i in range(2):
        df.plot(y=vars[i],ax=ax[i],color='red',marker='.')    

        # plot-wide adjustments
        ax[i].set_title(titles[i],linespacing=1.8)
        for b in ['top','right']: ax[i].spines[b].set_visible(False)
        ax[i].set_axisbelow(True)
        ax[i].get_legend().remove()

        # y-axis adjustments
        ax[i].yaxis.grid(True)
        ax[i].get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, '.0f')))
        ax[i].set_ylim(0,ylims[i])
        ax[i].set_ylabel(yaxes[i],rotation='horizontal')
        ax[i].yaxis.set_label_coords(-0.02,1.02)

        # x-axis adjustments
        ax[i].set_xlabel('')

        # annotations
        for v,c in zip([vars[i]],['red']):
            for j in range(len(df)):
                VAL = df[v].iloc[j]
                ADJ = 0.7 if vars[i] == 'pension' else 0.25
                ax[i].annotate(f'{VAL:.1f}',(df.index[j],VAL+ADJ),color=c,fontsize=8.8,ha='center')

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(TITLE)
        for i in range(len(df)): print(f'{df.index[i]}: RM{df["pension"].iloc[i]:.1f} bil ({df["pension_prop"].iloc[i]:.1f}%)')

    plt.savefig(f'output/{PATH}/timeseries_pension.png',dpi=400)
    plt.close()


print('')
timeseries_pension_politician()
print('')
bar_pension_politician()
print('')
bar_pension()
print('')
timeseries_pension()
print('')