import openmc
import numpy as np

A_Bank = 1  #0 is fully out 1 is fully in
B_Bank = 1  #0 is fully out 1 is fully in
C_Bank = 1  #0 is fully out 1 is fully in
Shut_Down_Bank = 1  #0 is fully out 1 is fully in
Batches = 2000
PPB = 10000
inactive = 200
Boron_PPM = 0
"""
n_axial = 40                # number of axial slices
z_bot = -100                 # bottom of active fuel
z_top = 143.84               # top of active fuel (m)
z_edges = np.linspace(z_bot, z_top, n_axial + 1)
z_centers = 0.5 * (z_edges[:-1] + z_edges[1:])

z_upper_edges = z_edges +z_top-z_bot

z_cr_edges = np.concatenate((z_edges[0:n_axial], z_upper_edges))
print(z_cr_edges[40])
"""

def axial_control_rod_fixed(p, n_total=81, n_guide=40, n_cr=40):
    """
    Returns an array of strings labeling each axial segment:
    ['guide', 'cr_guide', 'cr_water', 'water']
    - Always exactly n_cr cells are control rods
    - Rods are distributed between guide and water depending on insertion fraction p
    """

    assert 0.0 <= p <= 1.0

    # How many CR cells in guide tube
    n_cr_guide = int(round(p * n_guide))
    # How many CR cells in water box
    n_cr_water = n_cr - n_cr_guide

    regions = []

    for k in range(n_total):
        if k < n_guide:
            if k >= n_guide - n_cr_guide:
                regions.append('cr_guide')
            else:
                regions.append('guide')
        else:  # water region
            if k < n_guide + n_cr_water:
                regions.append('cr_water')
            else:
                regions.append('water')

    return np.array(regions)



"""regions = axial_control_rod_fixed(p=1)  # replace with your desired insertion fraction

# Count each type
unique, counts = np.unique(regions, return_counts=True)
count_dict = dict(zip(unique, counts))

print("Counts of each type:")
for key in ['cr_guide', 'cr_water', 'guide', 'water']:
    print(f"{key}: {count_dict.get(key, 0)}")"""