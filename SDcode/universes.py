import openmc
from cells import cells

universes = {}

universes['Root'] = openmc.Universe(universe_id=0,  name='Root')
universes['Root'].add_cells([cells['Core'],cells['lower plenum'],cells['upper plenum'],cells['core barrel'],cells['downcomer'],cells['rpv']])

universes['UO2L']  = openmc.Universe(universe_id=1,  name='UO2L')
universes['UO2M']  = openmc.Universe(universe_id=2,  name='UO2M')
universes['UO2H']  = openmc.Universe(universe_id=3,  name='UO2H')

universes['UO2L'].add_cells([cells['UO2L'], cells['gapL'], cells['cladL'], cells['moderatorL']])
universes['UO2M'].add_cells([cells['UO2M'], cells['gapM'], cells['cladM'], cells['moderatorM']])
universes['UO2H'].add_cells([cells['UO2H'], cells['gapH'], cells['cladH'], cells['moderatorH']])

#
## BP HE rod
universes['UO2HBP']  = openmc.Universe(universe_id=10,  name='UO2HBP')
universes['UO2HBP'].add_cells([cells['UO2HBP'],cells['IFBA'], cells['gapHBP'], cells['cladHBP'], cells['moderatorHBP']])


universes['guide tube'] = openmc.Universe(universe_id=4,  name='guide tube w CR')
universes['guide tube'].add_cells([cells['guide moderator'], cells['guide tube'], cells['moderatorG']])

universes['guide tube w CR'] = openmc.Universe(universe_id=11,  name='guide tube')
universes['guide tube w CR'].add_cells([cells['CRboron'], cells['cladCR'], cells['guide moderator w CR'], cells['guide tube CR'], cells['moderatorCR']])

universes['water cell'] = openmc.Universe(universe_id=5,  name='water cell')
universes['water cell'].add_cell(cells['water cell'] )


universes['UO2L Unrodded Assembly'] = openmc.Universe(universe_id=6,  name='UO2L Unrodded Assembly')
universes['UO2M Unrodded Assembly'] = openmc.Universe(universe_id=7,  name='UO2M Unrodded Assembly')
universes['UO2H Unrodded Assembly'] = openmc.Universe(universe_id=8,  name='UO2H Unrodded Assembly')
universes['UO2HBP1 Unrodded Assembly'] = openmc.Universe(universe_id=12, name='UO2HBP1 Unrodded Assembly')
universes['UO2HBP2 Unrodded Assembly'] = openmc.Universe(universe_id=14, name='UO2HBP2 Unrodded Assembly')

universes['UO2M rodded Assembly'] = openmc.Universe(universe_id=13,  name='UO2M rodded Assembly')
universes['UO2HBP2E rodded Assembly'] = openmc.Universe(universe_id=15, name='UO2HBP2E rodded Assembly')
universes['UO2HBP2S rodded Assembly'] = openmc.Universe(universe_id=16, name='UO2HBP2S rodded Assembly')
universes['UO2HBP2W rodded Assembly'] = openmc.Universe(universe_id=17, name='UO2HBP2W rodded Assembly')
universes['UO2HBP2N rodded Assembly'] = openmc.Universe(universe_id=18, name='UO2HBP2N rodded Assembly')

universes['UO2HBP2SE rodded Assembly'] = openmc.Universe(universe_id=19, name='UO2HBP2NE rodded Assembly')
universes['UO2HBP2SW rodded Assembly'] = openmc.Universe(universe_id=20, name='UO2HBP2SE rodded Assembly')
universes['UO2HBP2NW rodded Assembly'] = openmc.Universe(universe_id=21, name='UO2HBP2NW rodded Assembly')
universes['UO2HBP2NE rodded Assembly'] = openmc.Universe(universe_id=22, name='UO2HBP2NE rodded Assembly')

universes['UO2M Lrodded Assembly'] = openmc.Universe(universe_id=23,  name='UO2M Lrodded Assembly')
universes['UO2M Mrodded Assembly'] = openmc.Universe(universe_id=24,  name='UO2M Mrodded Assembly')

universes['UO2L Unrodded Assembly'].add_cell(cells['UO2L Unrodded Assembly'])
universes['UO2M Unrodded Assembly'].add_cell(cells['UO2M Unrodded Assembly'])
universes['UO2H Unrodded Assembly'].add_cell(cells['UO2H Unrodded Assembly'])
universes['UO2HBP1 Unrodded Assembly'].add_cell(cells['UO2HBP1 Unrodded Assembly'])
universes['UO2HBP2 Unrodded Assembly'].add_cell(cells['UO2HBP2 Unrodded Assembly'])

universes['UO2HBP2E rodded Assembly'].add_cell(cells['UO2HBP2E rodded Assembly'])
universes['UO2HBP2S rodded Assembly'].add_cell(cells['UO2HBP2S rodded Assembly'])
universes['UO2HBP2W rodded Assembly'].add_cell(cells['UO2HBP2W rodded Assembly'])
universes['UO2HBP2N rodded Assembly'].add_cell(cells['UO2HBP2N rodded Assembly'])


universes['UO2HBP2SE rodded Assembly'].add_cell(cells['UO2HBP2SE rodded Assembly'])
universes['UO2HBP2SW rodded Assembly'].add_cell(cells['UO2HBP2SW rodded Assembly'])
universes['UO2HBP2NE rodded Assembly'].add_cell(cells['UO2HBP2NE rodded Assembly'])
universes['UO2HBP2NW rodded Assembly'].add_cell(cells['UO2HBP2NW rodded Assembly'])

universes['UO2M rodded Assembly'].add_cell(cells['UO2M rodded Assembly'])
universes['UO2M Lrodded Assembly'].add_cell(cells['UO2M Lrodded Assembly'])
universes['UO2M Mrodded Assembly'].add_cell(cells['UO2M Mrodded Assembly'])

universes['Water Assembly'] = openmc.Universe(universe_id=9, name='Water Assembly')
universes['Water Assembly'].add_cell(cells['Water Assembly'])


#print(universes)
