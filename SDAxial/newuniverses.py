import openmc

from matax import *

universes = {}

universes['Root'] = openmc.Universe(name='Root')
universes['Root'].add_cells([cells['Core'],cells['lower plenum'],cells['upper plenum'],cells['core barrel'],cells['downcomer'],cells['rpv']])

universes['UO2L']  = openmc.Universe(name='UO2L')
universes['UO2M']  = openmc.Universe(name='UO2M')
universes['UO2H']  = openmc.Universe(name='UO2H')

universes['UO2L'].add_cells([cells['UO2L'], cells['gapL'], cells['cladL'], cells['moderatorL']])
universes['UO2M'].add_cells([cells['UO2M'], cells['gapM'], cells['cladM'], cells['moderatorM']])
universes['UO2H'].add_cells([cells['UO2H'], cells['gapH'], cells['cladH'], cells['moderatorH']])

universes['UO2HBP']  = openmc.Universe(name='UO2HBP')
universes['UO2HBP'].add_cells([cells['UO2HBP'],cells['IFBA'], cells['gapHBP'], cells['cladHBP'], cells['moderatorHBP']])

universes['guide tube'] = openmc.Universe(name='guide tube w CR')
universes['guide tube'].add_cells([cells['inner guide moderator no CR'], cells['guide tube'], cells['g_moderator1']])

universes['guide tube w CR'] = openmc.Universe(name='guide tube')
universes['guide tube w CR'].add_cells([cells['CRboron'], cells['cladCR'], cells['inner guide moderator w CR'], cells['guide tube CR'], cells['g_moderator2']])

universes['water cell'] = openmc.Universe(name='water cell')
universes['water cell'].add_cell(cells['water cell'] )

universes['inconel cell'] = openmc.Universe(name='inconel cell')
universes['inconel cell'].add_cell(cells['inconel cell'] )

universes['UO2L Unrodded Assembly'] = openmc.Universe( name='UO2L Unrodded Assembly')
universes['UO2M Unrodded Assembly'] = openmc.Universe(name='UO2M Unrodded Assembly')
universes['UO2H Unrodded Assembly'] = openmc.Universe(name='UO2H Unrodded Assembly')
universes['UO2HBP1 Unrodded Assembly'] = openmc.Universe(name='UO2HBP1 Unrodded Assembly')
universes['UO2HBP2 Unrodded Assembly'] = openmc.Universe(name='UO2HBP2 Unrodded Assembly')

universes['UO2M rodded Assembly'] = openmc.Universe(name='UO2M rodded Assembly')
universes['UO2HBP2S rodded Assembly'] = openmc.Universe(name='UO2HBP2S rodded Assembly')
universes['UO2HBP2W rodded Assembly'] = openmc.Universe(name='UO2HBP2W rodded Assembly')

universes['UO2HBP2SW rodded Assembly'] = openmc.Universe(name='UO2HBP2SE rodded Assembly')


universes['UO2M Lrodded Assembly'] = openmc.Universe(name='UO2M Lrodded Assembly')
universes['UO2M Mrodded Assembly'] = openmc.Universe(name='UO2M Mrodded Assembly')

universes['UO2L Unrodded Assembly'].add_cell(cells['UO2L Unrodded Assembly'])
universes['UO2M Unrodded Assembly'].add_cell(cells['UO2M Unrodded Assembly'])
universes['UO2H Unrodded Assembly'].add_cell(cells['UO2H Unrodded Assembly'])
universes['UO2HBP1 Unrodded Assembly'].add_cell(cells['UO2HBP1 Unrodded Assembly'])
universes['UO2HBP2 Unrodded Assembly'].add_cell(cells['UO2HBP2 Unrodded Assembly'])


universes['UO2HBP2S rodded Assembly'].add_cell(cells['UO2HBP2S rodded Assembly'])
universes['UO2HBP2W rodded Assembly'].add_cell(cells['UO2HBP2W rodded Assembly'])

universes['UO2HBP2SW rodded Assembly'].add_cell(cells['UO2HBP2SW rodded Assembly'])

universes['UO2M rodded Assembly'].add_cell(cells['UO2M rodded Assembly'])
universes['UO2M Lrodded Assembly'].add_cell(cells['UO2M Lrodded Assembly'])
universes['UO2M Mrodded Assembly'].add_cell(cells['UO2M Mrodded Assembly'])

universes['Water Assembly'] = openmc.Universe(name='Water Assembly')
universes['Water Assembly'].add_cell(cells['Water Assembly'])

universes['Baffle Assembly'] = openmc.Universe(name='Baffle Assembly')
universes['Baffle Assembly'].add_cell(cells['Baffle Assembly'])

#print(universes)