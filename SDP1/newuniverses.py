import openmc
from matax import *
from specialinputs import*
#from lattices import lattices

universes = {}

universes['Root'] = openmc.Universe(name='Root')
universes['Root'].add_cells([cells['Core'],cells['lower plenum'], cells['core barrel'], cells['core barrel replace'],cells['downcomer'],cells['rpv']])

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

universes['guide tube w CR'] = openmc.Universe(name='guide tube w CR')
universes['guide tube w CR'].add_cells([cells['B4C CR'], cells['cladCR'], cells['inner guide moderator w CR'], cells['guide tube CR'], cells['g_moderator3']])

universes['guide tube no CR'] = openmc.Universe(name='guide tube no CR')
universes['guide tube no CR'].add_cells([cells['inner guide moderator no CR'], cells['guide tube CR'], cells['g_moderator3']])

universes['CR above core'] = openmc.Universe(name='CR above core')
universes['CR above core'].add_cells([cells['B4C CR2'], cells['cladCR2'], cells['CR moderator above core']])

universes['water above core'] = openmc.Universe(name='water above core')
universes['water above core'].add_cell(cells['water above core'] )

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


z_planes_CR = []
for i, z in enumerate(z_cr_edges):
    zp = openmc.ZPlane(z0=z, name=f'z_cr_{i}')
    z_planes_CR.append(zp)


regions_A = axial_control_rod_fixed(A_Bank)
regions_B = axial_control_rod_fixed(B_Bank)
regions_C = axial_control_rod_fixed(C_Bank)
regions_Shut_Down = axial_control_rod_fixed(Shut_Down_Bank) 

bankA_cells = []
bankB_cells = []
bankC_cells = []
bank_Shut_Down_cells = []
#- 1
def make_axial_bank_cells(regions, bank_name):

    cells = []
    fill_map = {
        'cr_guide':  universes['guide tube w CR'],
        'guide':     universes['guide tube no CR'],
        'cr_water':  universes['CR above core'],
        'water':     universes['water above core'],
    }


    for i in range(len(z_cr_edges) - 1):
        cell = openmc.Cell(name=f'{bank_name}_axial_{i}')

        # Fill with appropriate universe
        cell.fill = fill_map[regions[i]]

        # Axial bounds
        cell.region = +z_planes_CR[i] & -z_planes_CR[i + 1]

        cells.append(cell)

    return cells

bankA_cells = make_axial_bank_cells(regions_A,'Bank_A')
bankB_cells = make_axial_bank_cells(regions_B,'Bank_B')
bankC_cells = make_axial_bank_cells(regions_C,'Bank_C')
bankShut_Down_cells = make_axial_bank_cells(regions_Shut_Down,'Bank_Shut_Down')



universes['Bank A'] = openmc.Universe(name = 'Bank A', cells = bankA_cells)
universes['Bank B'] = openmc.Universe(name = 'Bank B', cells = bankB_cells)
universes['Bank C'] = openmc.Universe(name = 'Bank C', cells = bankC_cells)
universes['Shut Down Bank'] = openmc.Universe(name = 'Shut Down Bank', cells = bankShut_Down_cells)


universes['UO2L Unrodded Assembly'] = openmc.Universe( name='UO2L Unrodded Assembly')
universes['UO2M Unrodded Assembly'] = openmc.Universe(name='UO2M Unrodded Assembly')
universes['UO2H Unrodded Assembly'] = openmc.Universe(name='UO2H Unrodded Assembly')
universes['UO2HBP1 Unrodded Assembly'] = openmc.Universe(name='UO2HBP1 Unrodded Assembly')
universes['UO2HBP2 Unrodded Assembly'] = openmc.Universe(name='UO2HBP2 Unrodded Assembly')
universes['UO2HBP2S rodded Assembly'] = openmc.Universe(name='UO2HBP2S rodded Assembly')
universes['UO2HBP2W rodded Assembly'] = openmc.Universe(name='UO2HBP2W rodded Assembly')
universes['UO2HBP2SW rodded Assembly'] = openmc.Universe(name='UO2HBP2SE rodded Assembly')
universes['UO2M rodded Assembly'] = openmc.Universe(name='UO2M rodded Assembly')
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

universes['Bank A Assembly'] = openmc.Universe( name='Bank A Assembly')
universes['Bank A Assembly'].add_cell(cells['Bank A Assembly'])
universes['Bank B Assembly'] = openmc.Universe( name='Bank B Assembly')
universes['Bank B Assembly'].add_cell(cells['Bank B Assembly'])
universes['Bank C Assembly'] = openmc.Universe( name='Bank C Assembly')
universes['Bank C Assembly'].add_cell(cells['Bank C Assembly'])
universes['Bank Shut Down Assembly'] = openmc.Universe( name='Bank Shut Down Assembly')
universes['Bank Shut Down Assembly'].add_cell(cells['Bank Shut Down Assembly'])



universes['Water Assembly'] = openmc.Universe(name='Water Assembly')
universes['Water Assembly'].add_cell(cells['Water Assembly'])

universes['Baffle Assembly'] = openmc.Universe(name='Baffle Assembly')
universes['Baffle Assembly'].add_cell(cells['Baffle Assembly'])





"""geometry = openmc.Geometry()
geometry.root_universe = universes['Bank C'] #universes['guide tube w CR'] #universes['CR above core']
geometry.export_to_xml()

# Start with the single materials (non-axial)
material_colors = {
    axial_materials['IFBA']: (102, 255, 102),               # light green
    axial_materials['Borosilicate Glass']: (204, 153, 255), # purple
    axial_materials['B4C']: (204, 10, 255), 
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


plot_1 = openmc.Plot()
plot_1.filename = 'cell plot'
plot_1.width = [250, 450] #[pitch, pitch] #[r_rpvouter, r_rpvouter]
plot_1.pixels = [4000, 4000]
plot_1.origin = [0,0,20]
#plot_1.width = [r_rpvouter/2,r_rpvouter/2,10] #[21.42,21.42] #[r_rpvouter/2,r_rpvouter/2,10]
plot_1.basis = 'xz'
plot_1.color_by = 'material'
#plot_1.colors = material_colors

plot_file = openmc.Plots([plot_1])
plot_file.export_to_xml()
openmc.plot_geometry()"""
