import openmc
from surfaces import *


tallies = {}
# Instantiate a tally mesh
mesh = openmc.RegularMesh(mesh_id=1)
mesh.dimension = [221, 221, 45]#221
mesh.lower_left = [-w/2, -w/2, z_min]
mesh.upper_right = [w/2, w/2, z_max]

# Instantiate some tally Filters
mesh_filter = openmc.MeshFilter(mesh)

# Instantiate the Tally
tallies['Mesh Rates'] = openmc.Tally(tally_id=1, name='tally 1')
tallies['Mesh Rates'].filters = [mesh_filter]
tallies['Mesh Rates'].scores = ['flux', 'fission', 'nu-fission']

tallies['Global Rates'] = openmc.Tally(tally_id=2, name='tally 2')
tallies['Global Rates'].scores = ['flux', 'fission', 'nu-fission']
tallies_file = openmc.Tallies(tallies.values())
tallies_file.export_to_xml()