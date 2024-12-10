import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from datetime import datetime


def heatmap():
    df = pd.read_excel('sgu.xlsx')
    df.age = df.age.fillna(' ')
    df = df.set_index('age')

    sb.set(font="Monospace")
    fig, ax = plt.subplots(figsize=[10,7])  # width, height

    # heatmap
    sb.heatmap(df,
            annot=True, fmt=",.0f",
            annot_kws={'fontsize': 9},
            cmap='Blues',
            cbar=False,
            cbar_kws={"shrink": .9}, ax=ax)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_facecolor('white')
    ax.set_title(f'Median Wage by Age Group (2010-2023)\n', fontsize=10.5, linespacing=2)

    # ticks
    plt.yticks(rotation=0)
    ax.tick_params(axis=u'both', which=u'both',
                length=0, labelsize=10, 
                labelbottom=False, labeltop=True,
                bottom=False, top=False)
    
    ALT = 1
    if ALT == 1:
        # Print values for each row
        for idx, row in df.iterrows():
            print(f"\nAge group {idx}:")
            for year, value in row.items():
                print(f"{year}: {value:,.0f}")

    plt.savefig('wages.webp', dpi=400, bbox_inches='tight')


if __name__ == '__main__':
    print('')
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('\nGenerating heatmap:')
    heatmap()
    print('')