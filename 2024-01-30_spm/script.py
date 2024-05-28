import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import os


def bar_calon_most():
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'students'
    pf = df.copy().sort_values(by=v).tail(16)
    col_pos = sb.color_palette('Purples', n_colors=len(pf)).as_hex()
    pf.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'SPM 2023: Mata Pelajaran\ndengan Calon Paling Ramai\n(drpd {TOTAL_2023:,.0f} calon baru)\n',linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f'  {pf[v].iloc[i]:,.0f}  ({pf[v].iloc[i]/TOTAL_2023*100:,.1f}%)' for i in range(len(pf))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(pf)):
            print(f'{i+1}) {pf.index[len(pf)-i-1]}: {labels[len(pf)-i-1].strip()}')

    plt.savefig(f'bar_calon_most.png',dpi=400)
    plt.close()


def bar_calon_least():
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'students'
    pf = df.copy().sort_values(by=v).head(16)
    col_pos = sb.color_palette('Purples_r', n_colors=len(pf)).as_hex()
    pf.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'SPM 2023: Mata Pelajaran\ndengan Calon Paling Sedikit\n(drpd {TOTAL_2023:,.0f} calon baru)\n',linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f'  {pf[v].iloc[i]:,.0f}' for i in range(len(pf))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(pf)):
            print(f'{len(pf)-i}) {pf.index[len(pf)-i-1]}: {labels[len(pf)-i-1].strip()}')

    plt.savefig(f'bar_calon_least.png',dpi=400)
    plt.close()


def bar_results_gagal():
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'g'
    pf = df.copy().sort_values(by=v).tail(16)
    col_pos = sb.color_palette('Reds', n_colors=len(pf)).as_hex()
    pf.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'SPM 2023: Mata Pelajaran\ndengan % Gagal Paling Tinggi\n',linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f'  {pf[v].iloc[i]:,.1f}%' for i in range(len(pf))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(pf)):
            print(f'{i+1}) {pf.index[len(pf)-i-1]}: {labels[len(pf)-i-1].strip()}')

    plt.savefig(f'bar_results_gagal.png',dpi=400)
    plt.close()


def bar_results_a():
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'a'
    pf = df[df.students >= 10000].copy().sort_values(by=v).tail(16)
    col_pos = sb.color_palette('Greens', n_colors=len(pf)).as_hex()
    pf.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    ax.set_title(f'SPM 2023: Mata Pelajaran\ndengan % A+/A/A- Paling Tinggi\n(sekurangnya 10,000 calon)\n',linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f'  {pf[v].iloc[i]:,.1f}%' for i in range(len(pf))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(pf)):
            print(f'{i+1}) {pf.index[len(pf)-i-1]}: {labels[len(pf)-i-1].strip()}')

    plt.savefig(f'bar_results_a.png',dpi=400)
    plt.close()


def bar_results_a_bahasa():
    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [5,7]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    v = 'a'
    pf = df[(df.index.str.contains('Bahasa')) & (df.students > 1)].copy().sort_values(by=v).tail(16)
    col_pos = sb.color_palette('Greens', n_colors=len(pf)).as_hex()
    pf.plot(kind='barh', width=0.7, y=v, edgecolor='black', lw=0, color=col_pos, ax=ax)

    # plot-wide adjustments
    SPACE = '                  '
    ax.set_title(f'{SPACE}SPM 2023: Mata Pelajaran Bahasa\n{SPACE}dengan % A+/A/A- Paling Tinggi\n',linespacing=1.8)
    for b in ['top','right','bottom']: ax.spines[b].set_visible(False)
    ax.spines['left'].set_color('grey')
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)

    # y-axis adjustments
    ax.set_ylabel('')

    # x-axis adjustments
    ax.set_xlabel('')
    ax.xaxis.grid(False)
    ax.get_xaxis().set_visible(False)
    for c in ax.containers:
        labels = [f'  {pf[v].iloc[i]:,.1f}% drpd {pf["students"].iloc[i]:,.0f} calon' for i in range(len(pf))]
        ax.bar_label(c, labels=labels,fontsize=10)

    # ALT-text
    ALT = 1
    if ALT == 1:
        print(ax.get_title().strip())
        for i in range(len(pf)):
            print(f'{i+1}) {pf.index[len(pf)-i-1]}: {labels[len(pf)-i-1].strip()}')

    plt.savefig(f'bar_results_a_bahasa.png',dpi=400)
    plt.close()


CURDIR = os.getcwd()
os.chdir(f'{CURDIR}/2024-01-30_spm/')

TOTAL_2023 = 383685

df = pd.read_excel(f'src.xlsx')
df = df[df.year == 2023].drop(['year','code'],axis=1).set_index('subject')

print('')
print(f'{len(df)} subjects and {TOTAL_2023:,} calon in total')
print('')
bar_calon_most()
print('')
bar_calon_least()
print('')
bar_results_gagal()
print('')
bar_results_a()
print('')
bar_results_a_bahasa()
print('')

os.chdir(CURDIR)