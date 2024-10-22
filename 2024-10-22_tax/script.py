import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def lorenz_income():
    df = pd.read_parquet('https://storage.data.gov.my/dashboards/incometax_interactive.parquet')
    df = df[(df.variable == 'income') & (df.state == 'Malaysia') & (df.type == 'all') & (df.age == 'all')][['percentile','value']]
    df.percentile = df.percentile + 1
    new_row = pd.DataFrame({'percentile': [0], 'value': [0]})
    df = pd.concat([new_row, df]).reset_index(drop=True).rename(columns={'value':'tax'})
    df['tax_cumul'] = df.tax.cumsum()
    df['perc_cumul'] = df.tax_cumul / df.tax.sum() * 100
    df['perc_cumul_inverse'] = 100 - df['perc_cumul']

    plt.rcParams.update({'font.size': 11,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6.5,6.5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    # Plot 'perc_cumul' as a line chart
    df.plot(kind='line',x='percentile',y='perc_cumul',color='black',linewidth=1,marker='o',markersize=3,ax=ax,zorder=2)
    ax.set_title('Malaysia: Distribution of Income Declared by Individuals\n(estimated from percentile-resolution data for 2022)',linespacing=1.8)
    ax.legend_.remove()
    for s in ['top','right']: ax.spines[s].set_visible(False)
    for spine in ax.spines.values(): spine.set_color('#d3d3d3')

    # axis adjustments
    ax.set_ylabel(f'% of Income\n',linespacing=0.8)
    ax.set_xlabel('\n% of Taxpayers',linespacing=0.8)
    for axis in ['x', 'y']:
        ax.tick_params(axis=axis, which='both', length=0)
        getattr(ax, f'{axis}axis').grid(True, alpha=0.2)
        getattr(ax, f'set_{axis}lim')(0, 101)
        if axis == 'x':
            getattr(ax, f'set_{axis}ticks')(np.concatenate([np.arange(0, 101, 10), [85,95]]))
        else:
            getattr(ax, f'set_{axis}ticks')(np.arange(0, 101, 10))

    # annotations
    prop_paid = {85:45, 90:35, 95:23, 99:7}
    for p in [85, 90, 95, 99]:
        y_value = df.iloc[p]['perc_cumul']
        ax.plot([0, p], [y_value, y_value], linewidth=1, alpha=0.7, color='red', zorder=1)
        ax.plot([p, p], [y_value, 0], linewidth=1, alpha=0.7, color='red', zorder=1)

        ax.annotate(f'T{100-p} made ~{prop_paid[p]}% of income', 
                    xy=(p-37, y_value), 
                    xytext=(p-37, y_value+2),
                    color='red',fontsize=10,va='center',ha='left')

    # # clarification note
    ax.text(0.03,0.25, """Data covers 4.2 mil tax filings only. 
    >50% of workers did not declare their income.""",
    fontstyle='italic',fontsize=8.5, linespacing=1.5, transform=ax.transAxes);

    plt.savefig('lorenz_income.webp',dpi=400)
    plt.close()


def lorenz_tax():
    df = pd.read_parquet('https://storage.data.gov.my/dashboards/incometax_interactive.parquet')
    df = df[(df.variable == 'tax') & (df.state == 'Malaysia') & (df.type == 'all') & (df.age == 'all')][['percentile','value']]
    df.percentile = df.percentile + 1
    new_row = pd.DataFrame({'percentile': [0], 'value': [0]})
    df = pd.concat([new_row, df]).reset_index(drop=True).rename(columns={'value':'tax'})
    df['tax_cumul'] = df.tax.cumsum()
    df['perc_cumul'] = df.tax_cumul / df.tax.sum() * 100
    df['perc_cumul_inverse'] = 100 - df['perc_cumul']

    plt.rcParams.update({'font.size': 11,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [6.5,6.5]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    # Plot 'perc_cumul' as a line chart
    df.plot(kind='line',x='percentile',y='perc_cumul',color='black',linewidth=1,marker='o',markersize=3,ax=ax,zorder=2)
    ax.set_title('Malaysia: Distribution of Tax Paid by Individuals\n(estimated from percentile-resolution data for 2022)',linespacing=1.8)
    ax.legend_.remove()
    for s in ['top','right']: ax.spines[s].set_visible(False)
    for spine in ax.spines.values(): spine.set_color('#d3d3d3')

    # axis adjustments
    ax.set_ylabel(f'% of Tax Paid\n',linespacing=0.8)
    ax.set_xlabel('\n% of Taxpayers',linespacing=0.8)
    for axis in ['x', 'y']:
        ax.tick_params(axis=axis, which='both', length=0)
        getattr(ax, f'{axis}axis').grid(True, alpha=0.2)
        getattr(ax, f'set_{axis}lim')(0, 101)
        if axis == 'x':
            getattr(ax, f'set_{axis}ticks')(np.concatenate([np.arange(0, 101, 10), [85,95]]))
        else:
            getattr(ax, f'set_{axis}ticks')(np.arange(0, 101, 10))

    # annotations
    prop_paid = {85:80, 90:70, 95:50, 99:20}
    for p in [85, 90, 95, 99]:
        y_value = df.iloc[p]['perc_cumul']
        ax.plot([0, p], [y_value, y_value], linewidth=1, alpha=0.7, color='red', zorder=1)
        ax.plot([p, p], [y_value, 0], linewidth=1, alpha=0.7, color='red', zorder=1)

        ax.annotate(f'T{100-p} paid ~{prop_paid[p]}% of taxes', 
                    xy=(p-35, y_value), 
                    xytext=(p-35, y_value+2),
                    color='red',fontsize=10,va='center',ha='left')

    # # clarification note
    ax.text(0.03,0.08, """Data covers 4.2 mil tax filings only.\n>50% of workers earned too little to be taxed.""",
    fontstyle='italic',fontsize=9, linespacing=1.5, transform=ax.transAxes);

    plt.savefig('lorenz_tax.webp',dpi=400)
    plt.close()

    ALT = 1
    if ALT == 1:
        ALT = """Line chart showing the cumulative distribution of tax paid by individuals in Malaysia.
The curve is steep at the higher percentiles, indicating a high concentration of tax payments among top earners.

Key visual elements:
1. The x-axis represents the percentage of taxpayers, from 0% to 100% at 10% intervals.
2. The y-axis shows the cumulative percentage of tax paid, from 0% to 100% at 10% intervals.
3. The chart uses a black line with small circular markers.
4. The x-axis includes additional tick marks at 85% and 95% to highlight the T15 and T5 statistics.

Key statistics:
- Top 15% (T15) paid ~80% of taxes
- Top 10% (T10) paid ~70% of taxes
- Top 5% (T5) paid ~50% of taxes
- Top 1% (T1) paid ~20% of taxes

Each of these points is marked with a red line extending from the y-axis to the curve, and then down to the x-axis.

Additional notes:
- The data covers 4.2 mil tax filings only. >50% of workers earned too little to be taxed.
- The data is estimated from percentile-resolution data for 2022.
"""

        print(ALT)


if __name__ == '__main__':
    print('')
    lorenz_income()
    print('')
    lorenz_tax()
    print('')