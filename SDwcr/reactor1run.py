import openmc
from matax import *
from lattices import lattices, universes, cells
from tally import tallies
from surfaces import *
import numpy as np
import os
from densitylookup import*
from fluxplot import xyslice , xzslice


#================================
# Cross sections
#================================
import os

# Path relative to the SDcode folder
libary_path = os.path.expanduser('~/Downloads/cross_section_libs/endfb-viii.0-hdf5/cross_sections.xml')


os.environ['OPENMC_CROSS_SECTIONS'] = libary_path

batches = 2006
inactive = 200 
particles = 10000





cells['Core'].region = -surfaces['inner core barrel']  & +surfaces['qc x'] & +surfaces['qc y']# &-surfaces['z-top active'] & +surfaces['z-bottom active']

#+surfaces['x-min'] & +surfaces['y-min'] & \-surfaces['x-max'] & -surfaces['y-max']


lattices['Core'] = openmc.RectLattice(name='7X7 core lattice')

lattices['Core'].dimension = [7, 7]
lattices['Core'].lower_left = [-w_ass/2, -w_ass/2]
lattices['Core'].pitch = [w_ass, w_ass]

#m=universes['Water Assembly']
m = universes['Baffle Assembly']
L=universes['UO2L Unrodded Assembly']
M=universes['UO2M Unrodded Assembly']
h=universes['UO2H Unrodded Assembly']
H=universes['UO2HBP1 Unrodded Assembly']
C=universes['UO2HBP2 Unrodded Assembly']
I=universes['UO2M rodded Assembly']
P=universes['UO2M Lrodded Assembly']
G=universes['UO2M Mrodded Assembly']
S=universes['UO2HBP2S rodded Assembly']
W=universes['UO2HBP2W rodded Assembly']
D=universes['UO2HBP2SW rodded Assembly']



lattices['Core'].universes=[
 [m,m,m,m,m,m,m],
 [H,H,C,m,m,m,m],
 [L,P,D,h,m,m,m],
 [G,L,P,P,h,m,m],
 [L,G,L,G,D,C,m],
 [I,L,G,L,P,H,m],
 [L,I,L,G,L,H,m]
]
cells['Core'].fill = lattices['Core']

universes['Core'] = openmc.Universe(name= 'Core', cells = [cells['Core']])

geometry = openmc.Geometry()
geometry.root_universe = universes['Core']
geometry.export_to_xml()


plot_1 = openmc.Plot()
plot_1.filename = 'cell plot'
plot_1.width = [r_rpvouter, r_rpvouter] #[pitch, pitch] #[r_rpvouter, r_rpvouter]
plot_1.pixels = [4000, 4000]
plot_1.origin = [r_rpvouter/2,r_rpvouter/2,150]
#plot_1.width = [r_rpvouter/2,r_rpvouter/2,10] #[21.42,21.42] #[r_rpvouter/2,r_rpvouter/2,10]
plot_1.basis = 'xy'
plot_1.color_by = 'material'

plot_file = openmc.Plots([plot_1])
plot_file.export_to_xml()
openmc.plot_geometry()


# Start with the single materials (non-axial)
material_colors = {
    axial_materials['IFBA']: (102, 255, 102),               # light green
    axial_materials['Borosilicate Glass']: (204, 153, 255), # purple
    axial_materials['Cladding']: (169, 169, 169),           # light gray
    axial_materials['SS304']: (192, 192, 192),              # silver
    axial_materials['Inconel']: (255, 153, 204),            # pink
    axial_materials['gap']: (0, 0, 0)                       # black
}

# Add all axial materials
for i in range(n_axial):
    material_colors[axial_materials[f'UO2L{i}']] = (255, 255, 102)       # pale yellow
    material_colors[axial_materials[f'UO2M{i}']] = (255, 178, 102)       # orange
    material_colors[axial_materials[f'UO2H{i}']] = (255, 51, 51)         # red
    material_colors[axial_materials[f'moderator{i}']] = (153, 204, 255)  # light blue


geometry = openmc.Geometry()
geometry.root_universe = universes['Root']
geometry.export_to_xml()

# surfaces: your dictionary of all defined surfaces
# geometry: your OpenMC Geometry object

# Step 1: get all surfaces actually used in cells
used_surfaces = geometry.get_all_surfaces()
#print(used_surfaces)
# Step 2: find all defined surfaces that are not used
unused_surfaces = [surf for surf in surfaces.values() if surf not in used_surfaces]


plot_1 = openmc.Plot()
plot_1.filename = 'plot_blue_water'
plot_1.width = [r_rpvouter, r_rpvouter] #[r_rpvouter, r_rpvouter]
plot_1.pixels = [4000, 4000]
plot_1.origin = [r_rpvouter/2,r_rpvouter/2,10] #[r_rpvouter/2,r_rpvouter/2,10]
plot_1.basis = 'xy'
plot_1.color_by = 'material'
#plot_1.universe_depth = 2  # important
plot_1.colors = material_colors

plot_2 = openmc.Plot()
plot_2.filename = 'plot_blue_water_w_spacers2'
plot_2.width = [r_rpvouter, r_rpvouter] #[r_rpvouter, r_rpvouter]
plot_2.pixels = [4000, 4000]
plot_2.origin = [r_rpvouter/2,r_rpvouter/2,-99]#[r_rpvouter/2,r_rpvouter/2,-99]
plot_2.basis = 'xy'
plot_2.color_by = 'material'
#plot_2.universe_depth = 2  # important
plot_2.colors = material_colors

plot_file = openmc.Plots([plot_1,plot_2])
plot_file.export_to_xml()
#openmc.plot_geometry()

lower_left = (0, 0, z_min)
upper_right = (hw, hw, z_max)
vol_calc = openmc.VolumeCalculation(list(axial_materials.values()), 100000000,
                                    lower_left, upper_right)

settings= openmc.Settings()
settings.batches=batches
settings.inactive=inactive
settings.particles=particles
settings.temperature = {
    'method': 'interpolation',
    'range': (293.0, 1800.0),
    'tolerance': 100.0
}

source = openmc.IndependentSource()

# Radial: uniform from 0 to R_core
r_dist = openmc.stats.Uniform(a=0.0, b=r_core)

# Azimuthal: uniform around the circle
phi_dist = openmc.stats.Uniform(a=0.0, b=(1/2)*np.pi)

# Axial: uniform over active height
z_dist = openmc.stats.Uniform(a=z_ba, b=z_ta)

source.space = openmc.stats.CylindricalIndependent(
    r=r_dist,
    phi=phi_dist,
    z=z_dist,
    origin=(0.0, 0.0, 0.0)  # center of the cylinder
)
source.only_fissionable = True
#source.constraints = {'fissionable': True}
#source.space = openmc.stats.Point([0,0,0])


settings.source = source
settings.volume_calculations = [vol_calc]
settings.export_to_xml()

tallies_file = openmc.Tallies(tallies.values())
tallies_file.export_to_xml()


#openmc.calculate_volumes()


#openmc.run()
xyslice(batches,20)
xyslice(batches,1)
xzslice(batches,1)