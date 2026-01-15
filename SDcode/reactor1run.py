import openmc
from materials import materials
from lattices import lattices, universes, cells
from tally import tallies
from surfaces import *
import numpy as np
import os
from fluxplot import xyslice


#================================
# Cross sections
#================================
import os

# Path relative to the SDcode folder
libary_path = os.path.expanduser('~/Downloads/cross_section_libs/endfb-viii.0-hdf5/cross_sections.xml')


os.environ['OPENMC_CROSS_SECTIONS'] = libary_path

batches = 2011
inactive = 500      
particles = 5000


materials_file = openmc.Materials(materials.values())
materials_file.export_to_xml()


cells['Core'].region = -surfaces['inner core barrel'] &-surfaces['z-top active'] & +surfaces['z-bottom active']

#+surfaces['x-min'] & +surfaces['y-min'] & \-surfaces['x-max'] & -surfaces['y-max']


lattices['Core'] = openmc.RectLattice(lattice_id=201, name='13x13 core lattice')

lattices['Core'].dimension = [13, 13]
lattices['Core'].lower_left = [-13/2*w_ass, -13/2*w_ass]
lattices['Core'].pitch = [w_ass, w_ass]

m=universes['Water Assembly']
L=universes['UO2L Unrodded Assembly']
M=universes['UO2M Unrodded Assembly']
h=universes['UO2H Unrodded Assembly']
H=universes['UO2HBP1 Unrodded Assembly']
C=universes['UO2HBP2 Unrodded Assembly']
P=universes['UO2M rodded Assembly']
G=universes['UO2M Lrodded Assembly']
I=universes['UO2M Mrodded Assembly']
E=universes['UO2HBP2E rodded Assembly']
S=universes['UO2HBP2S rodded Assembly']
W=universes['UO2HBP2W rodded Assembly']
N=universes['UO2HBP2N rodded Assembly']
A=universes['UO2HBP2NE rodded Assembly']
B=universes['UO2HBP2SE rodded Assembly']
D=universes['UO2HBP2SW rodded Assembly']
F=universes['UO2HBP2NW rodded Assembly']



lattices['Core'].universes=[
 [m,m,m,m,m,m,m,m,m,m,m,m,m],
 [m,m,m,m,h,C,C,C,h,m,m,m,m],
 [m,m,m,h,B,G,L,G,D,h,m,m,m],
 [m,m,h,L,G,L,I,L,G,L,h,m,m],
 [m,h,B,G,L,I,L,I,L,G,D,h,m],
 [m,C,G,L,I,L,I,L,I,L,G,C,m],
 [m,C,L,I,L,I,L,I,L,I,L,C,m],
 [m,C,G,L,I,L,I,L,I,L,G,C,m],
 [m,h,A,G,L,I,L,I,L,G,F,h,m],
 [m,m,h,L,G,L,I,L,G,L,h,m,m],
 [m,m,m,h,A,G,L,G,F,h,m,m,m],
 [m,m,m,m,h,C,C,C,h,m,m,m,m],
 [m,m,m,m,m,m,m,m,m,m,m,m,m]
]
cells['Core'].fill = lattices['Core']




geometry = openmc.Geometry()
geometry.root_universe = universes['Root']
geometry.export_to_xml()

plot_1 = openmc.Plot()
plot_1.filename = 'plot_blue_water'
plot_1.width = [r_rpvouter*2, r_rpvouter*2]
plot_1.pixels = [4000, 4000]
plot_1.origin = [0,0,0]
plot_1.basis = 'xy'
plot_1.color_by = 'material'
#plot_1.universe_depth = 2  # important
plot_1.colors = {
    materials['water']: (153, 204, 255),       # light blue
    materials['clad']: (169, 169, 169),        # light gray
    materials['UO2L']: (255, 255, 102),        # pale yellow
    materials['UO2M']: (255, 178, 102),        # orange
    materials['UO2H']: (255, 51, 51),          # red
    materials['IFBA']: (102, 255, 102),        # light green
    materials['boron rod']: (204, 153, 255),   # purple
    materials['SS304']: (192, 192, 192),       # silver
    materials['Inconel']: (255, 153, 204),      # pink
    materials['gap']: (0,0,0)                    #black
}
plot_file = openmc.Plots([plot_1])
plot_file.export_to_xml()
#openmc.plot_geometry()


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
phi_dist = openmc.stats.Uniform(a=0.0, b=2*np.pi)

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
settings.export_to_xml()

tallies_file = openmc.Tallies(tallies.values())
tallies_file.export_to_xml()



openmc.run()

xyslice(batches, 15)