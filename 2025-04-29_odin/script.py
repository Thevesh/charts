import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


df = pd.read_csv('odin.csv')
df['year'] = df.year.astype(str)
df = df.set_index('year').sort_index(ascending=True)
df.columns = [x.title() for x in df.columns]

fig, ax = plt.subplots(2,1,figsize=[5,6])  # width, height
plt.subplots_adjust(hspace=0.3)
ax[0].set_position([0.15, 0.4, 0.75, 0.5])  # [left, bottom, width, height]
ax[1].set_position([0.125, 0.14, 0.8, 0.2])  # [left, bottom, width, height]
ax = ax.ravel()

# timeseries for ranking
ax[0].plot(df.index, df['Ranking'], marker='o',markersize=4,color='black')
for b in ['top','right','bottom','left']: ax[0].spines[b].set_visible(False)
ax[0].invert_yaxis() # invert y-axis so 1 is at top
ax[0].set_ylim(104, -1) # set explicit limits
ax[0].grid(True, color='#c3c3c3', linestyle=':')
ax[0].set_title('Malaysia: ODIN Performance\n', fontsize=11, linespacing=1)
ax[0].set_yticks([1,21,41,61,81,101])
ax[0].set_ylabel('Rank\n(out of 197)',rotation=0,fontsize=11,linespacing=1.8)
ax[0].tick_params(axis='y', colors='white',length=0)
ax[0].tick_params(axis='x', colors='white',length=0)
ax[0].tick_params(axis='both', labelsize=10)
# add data labels
for i, txt in enumerate(df['Ranking']):
    OFFSETS = {
        97: 100,
        93: 96,
        64: 61,
        68: 65,
        78: 81,
        67: 70,
        1: 3
    }
    ax[0].annotate(f'{txt}', 
                   (df.index[i], OFFSETS[df['Ranking'].iloc[i]]),
                   xytext=(3, 0), 
                   textcoords='offset points',
                   fontsize=11,
                   va='center')

# heatmap
df.columns = [f'{x} ' for x in df.columns]
sb.heatmap(df.drop('Ranking ',axis=1).transpose(),
        annot=True, fmt=",.0f",
        annot_kws={'fontsize': 11},
        vmin = 0, vmax = 100,
        cmap='viridis',
        cbar=False,
        cbar_kws={"shrink": .9}, ax=ax[1])
ax[1].set_ylabel('')
ax[1].set_xlabel('\nScore (out of 100%)',fontsize=11,linespacing=0.3)
ax[1].set_facecolor('white')

# ticks
plt.yticks(rotation=0)
ax[1].tick_params(axis=u'both', which=u'both',
            length=0, labelsize=11, 
            labelbottom=False, labeltop=True,
            bottom=False, top=False)
plt.savefig('odin.png', dpi=300, bbox_inches='tight')
plt.close()