import openmc

from matax import *
#from lattices import lattices

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

universes['guide tube'] = openmc.Universe(name='guide tube')
universes['guide tube'].add_cells([cells['inner guide moderator no BPR'], cells['guide tube'], cells['g_moderator1']])

universes['guide tube w BPR'] = openmc.Universe(name='guide tube w BPR')
universes['guide tube w BPR'].add_cells([cells['BPRboron'], cells['cladBPR'], cells['inner guide moderator w BPR'], cells['guide tube BPR'], cells['g_moderator2']])

universes['water cell'] = openmc.Universe(name='water cell')
universes['water cell'].add_cell(cells['water cell'] )

universes['inconel cell'] = openmc.Universe(name='inconel cell')
universes['inconel cell'].add_cell(cells['inconel cell'] )

combinedcells = {}

combinedcells['UO2L Lower'] = openmc.Cell(name = 'UO2L Lower', fill= universes['UO2L'], region = outer_spacer_box & +surfaces['z-bottom active'] & -surfaces['z-top active'])
combinedcells['UO2L Upper'] = openmc.Cell(name= 'UO2L upper', fill = upper_water_fuel_univ, region= outer_spacer_box & +surfaces['z-top active'] & -surfaces['z-max'])
combinedcells['UO2M Lower'] = openmc.Cell(name = 'UO2M Lower', fill= universes['UO2M'], region = outer_spacer_box & +surfaces['z-bottom active'] & -surfaces['z-top active'])
combinedcells['UO2M Upper'] = openmc.Cell(name= 'UO2M upper', fill = upper_water_fuel_univ, region= outer_spacer_box & +surfaces['z-top active'] & -surfaces['z-max'])
combinedcells['UO2H Lower'] = openmc.Cell(name = 'UO2H Lower', fill= universes['UO2H'], region = outer_spacer_box & +surfaces['z-bottom active'] & -surfaces['z-top active'])
combinedcells['UO2H Upper'] = openmc.Cell(name= 'UO2H upper', fill = upper_water_fuel_univ, region= outer_spacer_box & +surfaces['z-top active'] & -surfaces['z-max'])
combinedcells['UO2HBP Lower'] = openmc.Cell(name = 'UO2HBP Lower', fill= universes['UO2HBP'], region = outer_spacer_box & +surfaces['z-bottom active'] & -surfaces['z-top active'])
combinedcells['UO2HBP Upper'] = openmc.Cell(name= 'UO2HBP upper', fill = upper_water_fuel_univ, region= outer_spacer_box & +surfaces['z-top active'] & -surfaces['z-max'])
combinedcells['guide tube w BPR Lower'] = openmc.Cell(name = 'guide tube w BPR Lower', fill= universes['guide tube w BPR'], region = outer_spacer_box & +surfaces['z-bottom active'] & -surfaces['z-top active'])
combinedcells['guide tube w BPR Upper'] = openmc.Cell(name= 'guide tube w BPR upper', fill = upper_water_fuel_univ, region= outer_spacer_box & +surfaces['z-top active'] & -surfaces['z-max'])
combinedcells['guide tube w/o BPR Lower'] = openmc.Cell(name = 'guide tube w/o BPR Lower', fill= universes['guide tube'], region = outer_spacer_box & +surfaces['z-bottom active'] & -surfaces['z-top active'])
combinedcells['guide tube w/o BPR Upper'] = openmc.Cell(name= 'guide tube w/o BPR upper', fill = upper_water_fuel_univ, region= outer_spacer_box & +surfaces['z-top active'] & -surfaces['z-max'])



universes['UO2L complete'] = openmc.Universe(name='UO2L complete', cells= [combinedcells['UO2L Lower'],combinedcells['UO2L Upper']])
universes['UO2M complete'] = openmc.Universe(name='UO2M complete', cells= [combinedcells['UO2M Lower'],combinedcells['UO2M Upper']])
universes['UO2H complete'] = openmc.Universe(name='UO2H complete', cells= [combinedcells['UO2H Lower'],combinedcells['UO2H Upper']])
universes['UO2HBP complete'] = openmc.Universe(name='UO2HBP complete', cells= [combinedcells['UO2HBP Lower'],combinedcells['UO2HBP Upper']])
universes['guide tube w BPR complete'] = openmc.Universe(name='guide tube w BPR complete', cells= [combinedcells['guide tube w BPR Lower'],combinedcells['guide tube w BPR Upper']])
universes['guide tube w/o BPR complete'] = openmc.Universe(name='guide tube w/o BPR complete', cells= [combinedcells['guide tube w/o BPR Lower'],combinedcells['guide tube w/o BPR Upper']])


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



