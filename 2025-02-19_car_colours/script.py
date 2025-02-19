import pandas as pd
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as tkr


def make_data():
    df = pd.DataFrame(columns=['year','colour','cars'])

    for i in range(2000,2025):
        tf = pd.read_parquet(f'https://storage.data.gov.my/transportation/cars_{i}.parquet',columns=['colour']).assign(cars=1)
        tf = tf.groupby(['colour']).sum().sort_values(by='cars',ascending=False).reset_index()
        tf['cars'] = tf['cars']/tf['cars'].sum() * 100
        if len(df) == 0:
            df = tf.assign(year=i).copy()[['year','colour','cars']]
        else:
            df = pd.concat([df,tf.assign(year=i)],axis=0,ignore_index=True)

    df.to_parquet('car_colours.parquet',index=False,compression='brotli')
    print(f'Saved to car_colours.parquet')


def stacked_bar(df=None):

    # Arranged to be aesthetically pleasing
    COLOURS = {
        # Achromatic colors
        'Black':    '#000000',
        'Greys':    '#A9A9A9',
        'White':    '#FFFFFF',
        
        # Cool colors
        'Blue':     '#0000FF',  
        'Purple':   '#800080',
        'Green':    '#00AA00',
        
        # Warm colors
        'Gold':     '#FFD700',
        'Yellow':   '#FFFF00',
        'Beige':    '#D4BE8D', 
        'Orange':   '#FF6600', 
        'Pink':     '#FF69B4',
        'Red':      '#FF0000',
        'Maroon':   '#800000',
        'Brown':    '#8B4513',
    }

    plt.rcParams.update({'font.size': 10,
                        'font.family': 'sans-serif',
                        'grid.linestyle': 'dashed'})
    plt.rcParams["figure.figsize"] = [9,8]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    df.plot(y=list(COLOURS.keys()), ax=ax, color=list(COLOURS.values()), 
            kind='bar', stacked=True, lw=0.6, edgecolor='#cccccc', width=0.9)

    # plot-wide adjustments
    ax.set_title("Malaysia: Registered Cars by Colour (2000-2024)\n",linespacing=1)
    for b in ['top','right','left']: ax.spines[b].set_visible(False)
    for b in ['left','bottom']: ax.spines[b].set_color('#cccccc')
    ax.set_axisbelow(True)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    ax.grid(False)
    ax.legend(bbox_to_anchor=(1.02, 0.5), loc='center left', frameon=False, labelspacing=1.1)

    # y-axis adjustments
    ax.set_ylabel('')
    ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(x, ',.0f') + '%'))
    ax.yaxis.set_ticks(np.arange(0, 101, 10))
    ax.set_ylim(0,100)

    # x-axis adjustments
    ax.set_xlabel('')

    print('\nALT text:')
    for c in list(COLOURS.keys()):
        print(f'{c}: {df.loc[2000,c]:.0f}% in 2000, {df.loc[2024,c]:.1f}% in 2024')
    
    for ext in ['png','webp']:
        plt.savefig(f'stacked_bar.{ext}',dpi=400,bbox_inches='tight')
    
    plt.close()
    return COLOURS



if __name__ == '__main__':
    print(f'Start: {datetime.now():%Y-%m-%d %H:%M:%S}')

    # print(f'\nWrangling from data.gov.my')
    # make_data()

    print(f'\nTransforming from saved file')
    df = pd.read_parquet('car_colours.parquet')\
        .pivot(index='colour',columns='year',values='cars')\
        .sort_values(by=2024)\
        .fillna(0)\
        .transpose()\
        .drop('unknown',axis=1)
    df.columns = [f'{c.title()}' for c in df.columns]
    df['Greys'] = df['Silver'] + df['Grey'] + df['Titanium']
    df = df.drop(['Silver','Grey','Titanium'],axis=1)

    print(f'\nPlotting')
    stacked_bar(df=df)

    print(f'\nEnd: {datetime.now():%Y-%m-%d %H:%M:%S}\n')
