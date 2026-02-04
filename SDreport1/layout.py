
import matplotlib.font_manager as fm

"""available_fonts = sorted(set(f.name for f in fm.fontManager.ttflist))
for f in available_fonts:
    print(f)"""

# Letters in lattice → enrichment type
enrichment_map = {
    'L':'Lowest Enrichment',
    'M':'Medium Enrichment',
    'H':'Highest Enrichment',
    'm':'Not Fuel'
}

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams['font.family'] = 'Nimbus Roman'

core = [
 ['m','m','m','m','m','m','m'],
 ['H','H','H','m','m','m','m'],
 ['L','M','H','H','m','m','m'],
 ['M','L','M','M','H','m','m'],
 ['L','M','L','M','H','H','m'],
 ['M','L','M','L','M','H','m'],
 ['L','M','L','M','L','H','m']
]

# Colors per enrichment type
colors = {'Lowest Enrichment':'yellow','Medium Enrichment':'orange','Highest Enrichment':'red','Not Fuel':'lightgrey'}

fig, ax = plt.subplots(figsize=(7,7))
n_rows = len(core)
n_cols = len(core[0])

for i in range(n_rows):
    for j in range(n_cols):
        letter = core[i][j]
        enrich = enrichment_map.get(letter,'Unknown')
        rect = plt.Rectangle((j, n_rows-1-i), 1, 1, facecolor=colors[enrich], edgecolor='black')
        ax.add_patch(rect)
        #ax.text(j+0.5, n_rows-1-i+0.5, letter, ha='center', va='center', fontsize=10)  # still show letter in cell

ax.set_xlim(0, n_cols)
ax.set_ylim(0, n_rows)
ax.set_aspect('equal')
ax.axis('off')

# Create legend based on enrichment type
legend_elements = [Patch(facecolor=v, edgecolor='black', label=k) for k,v in colors.items()]
ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10  )

#plt.title("Core Fuel Enrichment")
plt.tight_layout()
plt.savefig('Figure_1.png')
plt.show()


import matplotlib.pyplot as plt

# Example BA core mapping: None = no BA, otherwise 'D:#' or 'I:#'
ba_core = [
 ['None','None','None','None','None','None','None'],
 ['SD','SD','No CR','None','None','None','None'],
 ['C','No CR','No CR','SD','None','None','None'],
 ['No CR','A','No CR','No CR','SD','None','None'],
 ['B','No CR','C','No CR','No CR','No CR','None'],
 ['No CR','SD','No CR','A','No CR','SD','None'],
 ['A','No CR','B','No CR','C','SD','None']
]

n_rows = len(ba_core)
n_cols = len(ba_core[0])

fig, ax = plt.subplots(figsize=(7,7))

for i in range(n_rows):
    for j in range(n_cols):
        val = ba_core[i][j]
        if val != 'None':
            # Draw empty rectangle with black edge
            rect = plt.Rectangle((j, n_rows-1-i), 1, 1, facecolor='white', edgecolor='black', lw=1.5)
            ax.add_patch(rect)
            # Label with the BA type and number
            ax.text(j+0.5, n_rows-1-i+0.5, val, ha='center', va='center', fontsize=14)

ax.set_xlim(0, n_cols)
ax.set_ylim(0, n_rows)
ax.set_aspect('equal')
ax.axis('off')
#plt.title("Burnable Absorbers in Core")
plt.tight_layout()
plt.savefig('Figure_2.png')
plt.show()


# Example BA core mapping: None = no BA, otherwise 'D:#' or 'I:#'
ba_core = [
 ['None','None','None','None','None','None','None'],
 ['I:112','I:72','I:60','None','None','None','None'],
 ['No BA','D:20','D:9 I:72','I:72','None','None','None'],
 ['D:24','No BA','D:24','D:16','I:72','None','None'],
 ['No BA','D:24','No BA','D:24','D:9 I:72','I:60','None'],
 ['D:24','No BA','D:24','No BA','D:20','I:72','None'],
 ['No BA','D:24','No BA','D:24','No BA','I:112','None']
]

n_rows = len(ba_core)
n_cols = len(ba_core[0])

fig, ax = plt.subplots(figsize=(7,7))

for i in range(n_rows):
    for j in range(n_cols):
        val = ba_core[i][j]
        if val != 'None':
            # Draw empty rectangle with black edge
            rect = plt.Rectangle((j, n_rows-1-i), 1, 1, facecolor='white', edgecolor='black', lw=1.5)
            ax.add_patch(rect)
            # Label with the BA type and number
            ax.text(j+0.5, n_rows-1-i+0.5, val, ha='center', va='center', fontsize=14)

ax.set_xlim(0, n_cols)
ax.set_ylim(0, n_rows)
ax.set_aspect('equal')
ax.axis('off')
#plt.title("Burnable Absorbers in Core")
plt.tight_layout()
plt.savefig('Figure_3.png')
plt.show()