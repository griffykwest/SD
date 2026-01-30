import numpy as np
import openmc
from densitylookup import *
import os
from specialinputs import axial_control_rod_fixed
from tally import tallies
from surfaces import *
from fluxplot import xyslice , xzslice
from PPF import ppf

def run_model(
    A_Bank=0.0,
    B_Bank=0.0,
    C_Bank=0.0,
    Shut_Down_Bank=0.0,
    Batches=2000,
    PPB=10000,
    inactive=50,
    Boron_PPM=2250
    ):
    ##set run variables here this will change specialinputs 

    libary_path = os.path.expanduser('~/Downloads/cross_section_libs/endfb-viii.0-hdf5/cross_sections.xml')


    os.environ['OPENMC_CROSS_SECTIONS'] = libary_path

    # ----------------------------
    # Axial parameters
    # ----------------------------
    n_axial = 40                # number of axial slices
    z_bot = -100                 # bottom of active fuel
    z_top = 143.84               # top of active fuel (m)
    z_edges = np.linspace(z_bot, z_top, n_axial + 1)
    z_centers = 0.5 * (z_edges[:-1] + z_edges[1:])

    z_upper_edges = z_edges +z_top-z_bot

    z_cr_edges = np.concatenate((z_edges[0:n_axial], z_upper_edges))
    #print(z_cr_edges[40])
    h = np.linspace(0, 1, n_axial)  # normalized axial position 0->1

    T_min = 700
    T_max = 700

    T_avg = (T_max + T_min) / 2
    T_amp = (T_max + T_min) / 2

    # Cosine shape, peak in the middle, edges at min
    T_fuel_z = T_min + T_amp * np.cos(np.pi * (h - 0.5))

    T_mod_z  = np.linspace(290+273.15, 310+273.15, n_axial)


    axial_materials = {}
    multiplier = 1.0
    fuel_density = 10.30
    for i in range(n_axial):

        uo2l=openmc.Material()
        uo2l.name=f'UO2L{i}'
        lenrichment=2.25*multiplier
        uo2l.add_element('U',1.0,enrichment=lenrichment)
        uo2l.add_element('O',2.0)
        uo2l.set_density('g/cm3',fuel_density) #****
        uo2l.temperature = T_fuel_z[i]
        axial_materials[f'UO2L{i}']  = uo2l

        uo2m=openmc.Material()
        uo2m.name=f'UO2M{i}'
        menrichment=3.5*multiplier
        uo2m.add_element('U',1.0,enrichment=menrichment)
        uo2m.add_element('O',2.0)
        uo2m.set_density('g/cm3',fuel_density) #****
        uo2m.temperature = T_fuel_z[i]
        axial_materials[f'UO2M{i}']  = uo2m

        uo2h=openmc.Material()
        uo2h.name=f'UO2H{i}'
        henrichment=4.75*multiplier
        uo2h.add_element('U',1.0,enrichment=henrichment)
        uo2h.add_element('O',2.0)
        uo2h.set_density('g/cm3',fuel_density) #****
        uo2h.temperature = T_fuel_z[i]
        axial_materials[f'UO2H{i}']  = uo2h



        watertempc = T_mod_z[i]-273.15
        density = 1/pl('T',watertempc, 'vol_f')
        density = density/1000

        moderator = openmc.Material()
        moderator.name= f'moderator{i}'
        moderator.add_element('H', 2.0)
        moderator.add_element('O', 1.0)
        moderator.add_element('B', Boron_PPM * 1e-6)
        moderator.set_density('g/cm3', density)
        moderator.temperature = T_mod_z[i]
        axial_materials[f'moderator{i}']  = moderator




    #natural enriched B10 is 19.9
    B10enrichment= 0.2 # for rods
    B10_enr = 0.2 # for coating
    ##IFBA inspired coating from math the coating should be about 10 micronsbut the gap is only 5 microns? so maybe just a little less
    IFBA=openmc.Material()
    IFBA.name = 'IFBA'
    IFBA.add_nuclide('B10', 2.0 * B10_enr)
    IFBA.add_nuclide('B11', 2.0 * (1.0 - B10_enr))
    IFBA.add_element('Zr',1.0)
    IFBA.set_density('g/cm3',6.09)

    ###Cladding
    zirc = (99.83-1.03)/100
    clad=openmc.Material()
    clad.name='Cladding'
    #clad.add_element('Sn',1.45/100,'wo')
    clad.add_element('Fe',0.035/100,'wo')
    clad.add_element('Cr',0.005/100,'wo')
    clad.add_element('Zr',zirc,'wo')
    clad.add_element('O',0.13,'wo')
    clad.add_element('Nb',1.03/100,'wo')
    clad.set_density('g/cm3',6.52)

    inconel = openmc.Material()
    inconel.name ="Inconel"
    inconel.add_element("Ni", 52.0/100, percent_type="wo")
    inconel.add_element("Cr", 19.0/100, percent_type="wo")
    inconel.add_element("Nb", 5.0/100, percent_type="wo")
    inconel.add_element("Mo", 3.0/100, percent_type="wo")
    inconel.add_element("Ti", 0.75/100, percent_type="wo")
    inconel.add_element("Al", 0.4/100, percent_type="wo")
    inconel.add_element("Co", 0.5/100, percent_type="wo")
    inconel.add_element("Mg", 0.25/100, percent_type="wo")
    inconel.add_element("Si", 0.025/100, percent_type="wo")
    inconel.add_element("P",  0.0075/100, percent_type="wo")
    inconel.add_element("S",  0.0075/100, percent_type="wo")
    inconel.add_element("C",  0.15/100, percent_type="wo")
    inconel.add_element("Fe", 18.91/100, percent_type="wo")

    inconel.set_density("g/cm3", 8.19)

    ##STST for Gray rods maybe,  and as cladding for control rods https://www.thyssenkrupp-materials.co.uk/stainless-steel-304-14301.html
    C  = 0.07
    Cr = 18.5
    Mn = 2.0
    Si = 1.0
    P  = 0.045
    S  = 0.015
    Ni = 9.25
    N  = 0.10

    Fe = 100 - (C + Cr + Mn + Si + P + S + Ni + N)
    ss304 = openmc.Material()
    ss304.name = "SS304"
    ss304.add_element("C",  C/100,  percent_type="wo")
    ss304.add_element("Cr", Cr/100, percent_type="wo")
    ss304.add_element("Mn", Mn/100, percent_type="wo")
    ss304.add_element("Si", Si/100, percent_type="wo")
    ss304.add_element("P",  P/100,  percent_type="wo")
    ss304.add_element("S",  S/100,  percent_type="wo")
    ss304.add_element("Ni", Ni/100, percent_type="wo")
    ss304.add_element("N",  N/100,  percent_type="wo")
    ss304.add_element("Fe", Fe/100, percent_type="wo")
    ss304.set_density("g/cm3", 8.0)

    ##moving Control rods Ag-In-Cd or boroscilate glass



    #  Boriscilate glass for constant rods that go in and stay in new and second ran fuels

    # Boron-10 enrichment (fraction of boron atoms)
    B10enrichment = 0.4  # example: 40% B-10
    borosilicate = openmc.Material(name='Borosilicate Glass')
    borosilicate.set_density('g/cm3', 2.23)
    # --- Boron (atomic fraction split into isotopes) ---
    B_total = 0.070449
    borosilicate.add_nuclide(
        'B10', B_total * B10enrichment, percent_type='ao'
    )
    borosilicate.add_nuclide(
        'B11', B_total * (1.0 - B10enrichment), percent_type='ao'
    )
    # --- Remaining elements (atomic fractions, unchanged) ---
    borosilicate.add_element('O',  0.641095, percent_type='ao')
    borosilicate.add_element('Na', 0.023311, percent_type='ao')
    borosilicate.add_element('Al', 0.008204, percent_type='ao')
    borosilicate.add_element('Si', 0.255327, percent_type='ao')
    borosilicate.add_element('K',  0.001615, percent_type='ao')

    """openmc.Material(name='Borosilicate Glass') 
    borosilicate.set_density('g/cm3', 2.23) 
    B10 = B10enrichment*0.04 
    B11 = (1-B10enrichment)*0.04 
    borosilicate.add_nuclide('B10', B10, percent_type='wo') 
    borosilicate.add_nuclide('B11', B11, percent_type='wo') # Rest of the glass (fixed) 
    #borosilicate.add_element('B', 0.04, percent_type='wo') 
    # borosilicate.add_element('O', 0.535, percent_type='wo') 
    # borosilicate.add_element('Si', 0.377, percent_type='wo') 
    # borosilicate.add_element('Na', 0.030, percent_type='wo') 
    borosilicate.add_element('Al', 0.012, percent_type='wo')"""


    B10enrichmentB4C = 0.20  # 20% B-10, adjust as needed
    B4C = openmc.Material(name='Boron Carbide (B4C)')
    B4C.set_density('g/cm3', 2.52)

    B_total = 0.799981

    B4C.add_nuclide('B10', B_total * B10enrichmentB4C, percent_type='ao')
    B4C.add_nuclide('B11', B_total * (1.0 - B10enrichmentB4C), percent_type='ao')
    B4C.add_element('C', 0.200019, percent_type='ao')

    gap = openmc.Material(name='gap')
    gap.add_element('He', 1.0)
    gap.set_density('g/cm3', 0.001)

    axial_materials['IFBA'] = IFBA
    axial_materials['Borosilicate Glass'] = borosilicate
    axial_materials['B4C'] = B4C
    axial_materials['Cladding'] = clad
    axial_materials['SS304'] = ss304
    axial_materials['Inconel'] = inconel
    axial_materials['gap'] = gap

    materials_file = openmc.Materials(axial_materials.values())
    materials_file.export_to_xml()

    ##print(axial_materials)

    z_planes = [openmc.ZPlane(z0=z) for z in z_edges]
    spacer_indices = [0, 9, 19, 29, 39]
    axial_cells = {}



    for i in range(n_axial):
        z_bottom = +z_planes[i]    # everything above z_bottom
        z_top    = -z_planes[i+1]  # everything below z_top

        spacer_region = (
        -surfaces['outer spacer x-max'] & +surfaces['outer spacer x-min'] &
        -surfaces['outer spacer y-max'] & +surfaces['outer spacer y-min'] &
        ~(
            -surfaces['spacer x-max'] & +surfaces['spacer x-min'] &
            -surfaces['spacer y-max'] & +surfaces['spacer y-min']
        ) &
        +z_planes[i] & -z_planes[i+1]  # axial bounds
    )
        axial_cells[f'UO2L{i}'] = openmc.Cell(name = f'UO2L{i}', fill= axial_materials[f'UO2L{i}'], region=-surfaces['pin radius'] & z_bottom & z_top)
        axial_cells[f'UO2L{i}'].temperature = axial_materials[f'UO2L{i}'].temperature

        axial_cells[f'UO2M{i}'] = openmc.Cell(name = f'UO2M{i}', fill= axial_materials[f'UO2M{i}'], region=-surfaces['pin radius'] & z_bottom & z_top)
        axial_cells[f'UO2M{i}'].temperature = axial_materials[f'UO2M{i}'].temperature

        axial_cells[f'UO2H{i}'] = openmc.Cell(name = f'UO2H{i}', fill= axial_materials[f'UO2H{i}'], region=-surfaces['pin radius'] & z_bottom & z_top)
        axial_cells[f'UO2H{i}'].temperature = axial_materials[f'UO2H{i}'].temperature

        if i in spacer_indices:
            axial_cells[f'moderator{i}'] = openmc.Cell(name = f'moderator{i}', fill= axial_materials[f'moderator{i}'], region=+surfaces['cladding outer radius'] & z_bottom & z_top & spacer_box)
            axial_cells[f'moderator{i}'].temperature = axial_materials[f'moderator{i}'].temperature

            axial_cells[f'guide moderator{i}'] = openmc.Cell(name = f'guide moderator{i}', fill= axial_materials[f'moderator{i}'], region=+surfaces['guide outer radius'] & z_bottom & z_top & spacer_box)
            axial_cells[f'guide moderator{i}'].temperature = axial_materials[f'moderator{i}'].temperature

            axial_cells[f'spacer{i}'] = openmc.Cell(name= f'spacer{i}', fill = axial_materials['Inconel'], region= spacer_region)
            axial_cells[f'g spacer{i}'] = openmc.Cell(name= f'g spacer{i}', fill = axial_materials['Inconel'], region=spacer_region)
        else:
            axial_cells[f'moderator{i}'] = openmc.Cell(name = f'moderator{i}', fill= axial_materials[f'moderator{i}'], region=+surfaces['cladding outer radius'] & z_bottom & z_top)
            axial_cells[f'moderator{i}'].temperature = axial_materials[f'moderator{i}'].temperature

            axial_cells[f'guide moderator{i}'] = openmc.Cell(name = f'guide moderator{i}', fill= axial_materials[f'moderator{i}'], region=+surfaces['guide outer radius'] & z_bottom & z_top)
            axial_cells[f'guide moderator{i}'].temperature = axial_materials[f'moderator{i}'].temperature


        axial_cells[f'inner guide moderator no BPR{i}'] = openmc.Cell(name = f'inner guide moderator no BPR{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['guide inner radius'] & z_bottom & z_top)
        axial_cells[f'inner guide moderator no BPR{i}'].temperature = axial_materials[f'moderator{i}'].temperature

        axial_cells[f'inner guide moderator w BPR{i}'] = openmc.Cell(name = f'inner guide moderator w BPR{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['guide inner radius'] & +surfaces['BPR rod cladding outer radius'] & z_bottom & z_top)
        axial_cells[f'inner guide moderator w BPR{i}'].temperature = axial_materials[f'moderator{i}'].temperature



    uo2l_axial_cells = []
    uo2m_axial_cells = []
    uo2h_axial_cells = []
    spacer_axial_cells = []
    moderator_axial_cells = []
    g_moderator_axial_cells = []
    i_g_moderator_axial_cells_n_BPR = []
    i_g_moderator_axial_cells_w_BPR = []

    axial_cells['upper water cell fuel'] = openmc.Cell(name= 'upper water cell fuel box', fill= axial_materials['moderator39'], region= +surfaces['z-top active'] & -surfaces['z-max']& outer_spacer_box)


    for i in range(n_axial):
        uo2l_axial_cells.append(axial_cells[f'UO2L{i}'])
        uo2m_axial_cells.append(axial_cells[f'UO2M{i}'])
        uo2h_axial_cells.append(axial_cells[f'UO2H{i}'])
        moderator_axial_cells.append(axial_cells[f'moderator{i}'])
        g_moderator_axial_cells.append(axial_cells[f'guide moderator{i}'])
        if i in spacer_indices:
            moderator_axial_cells.append(axial_cells[f'spacer{i}'])
            g_moderator_axial_cells.append(axial_cells[f'g spacer{i}'])
        i_g_moderator_axial_cells_n_BPR.append(axial_cells[f'inner guide moderator no BPR{i}'])
        i_g_moderator_axial_cells_w_BPR.append(axial_cells[f'inner guide moderator w BPR{i}'])

    UO2L_cont_universe = openmc.Universe(cells=uo2l_axial_cells)
    UO2M_cont_universe = openmc.Universe(cells=uo2m_axial_cells)
    UO2H_cont_universe = openmc.Universe(cells=uo2h_axial_cells)
    moderator_cont_universe = openmc.Universe(cells=moderator_axial_cells)

    g_moderator_cont_universe = openmc.Universe(cells=g_moderator_axial_cells)
    i_g_moderator_n_BPR_cont_universe = openmc.Universe(cells=i_g_moderator_axial_cells_n_BPR)
    i_g_moderator_w_BPR_cont_universe = openmc.Universe(cells=i_g_moderator_axial_cells_w_BPR)
    upper_water_fuel_univ = openmc.Universe(cells = [axial_cells['upper water cell fuel']])


    ##print(spacer_cont_universe)
    cells = {}
    cells['UO2L'] = openmc.Cell(name='UO2L', region = -surfaces['pin radius'], fill = UO2L_cont_universe)
    cells['UO2M'] = openmc.Cell(name='UO2M', region = -surfaces['pin radius'], fill = UO2M_cont_universe)
    cells['UO2H'] = openmc.Cell(name='UO2H', region = -surfaces['pin radius'], fill = UO2H_cont_universe)
    cells['UO2HBP'] = openmc.Cell(name='UO2HBP', region = -surfaces['pin radius'], fill = UO2H_cont_universe)
    cells['moderatorL'] = openmc.Cell(name='moderatorL', region = +surfaces['cladding outer radius'], fill = moderator_cont_universe)
    cells['moderatorM'] = openmc.Cell(name='moderatorM', region = +surfaces['cladding outer radius'], fill = moderator_cont_universe)
    cells['moderatorH'] = openmc.Cell(name='moderatorH', region = +surfaces['cladding outer radius'], fill = moderator_cont_universe)
    cells['moderatorHBP'] = openmc.Cell(name='moderatorHBP', region = +surfaces['cladding outer radius'], fill = moderator_cont_universe)
    cells['g_moderator1'] = openmc.Cell(name='g_moderator1', region = +surfaces['guide outer radius'], fill = g_moderator_cont_universe)
    cells['g_moderator2'] = openmc.Cell(name='g_moderator2', region = +surfaces['guide outer radius'], fill = g_moderator_cont_universe)
    cells['g_moderator3'] = openmc.Cell(name='g_moderator3', region = +surfaces['guide outer radius'], fill = g_moderator_cont_universe)
    cells['g_moderator4'] = openmc.Cell(name='g_moderator4', region = +surfaces['guide outer radius'], fill = g_moderator_cont_universe)
    cells['inner guide moderator no CR'] = openmc.Cell(name='inner guide moderator no CR', region = -surfaces['guide inner radius'], fill = i_g_moderator_n_BPR_cont_universe)
    cells['inner guide moderator no BPR'] = openmc.Cell(name='inner guide moderator no BPR', region = -surfaces['guide inner radius'], fill = i_g_moderator_n_BPR_cont_universe)
    cells['inner guide moderator w BPR'] = openmc.Cell(name='inner guide moderator w BPR', region = -surfaces['guide inner radius'] & +surfaces['BPR rod cladding outer radius'], fill = i_g_moderator_w_BPR_cont_universe)
    cells['inner guide moderator w CR'] = openmc.Cell(name='inner guide moderator w CR', region = -surfaces['guide inner radius'] & +surfaces['BPR rod cladding outer radius'], fill = i_g_moderator_w_BPR_cont_universe)

    """#print(cells['spacerL'])
    #print(cells['UO2L'])
    #print(cells['moderatorHBP'])"""

    #IFBA coating on high enriched
    cells['IFBA'] = openmc.Cell(name='IFBA')
    cells['IFBA'].region = -surfaces['IFBA'] & +surfaces['pin radius'] 
    cells['IFBA'].fill = axial_materials['IFBA']

    #Integral control rod
    cells['BPRboron'] = openmc.Cell(name = 'BPRboron')
    cells['BPRboron'].fill = axial_materials['Borosilicate Glass']
    cells['BPRboron'].region = -surfaces['BPR rod cladding inner radius'] 

    cells['B4C CR'] = openmc.Cell(name = 'B4C CR')
    cells['B4C CR'].fill = axial_materials['B4C']
    cells['B4C CR'].region = -surfaces['BPR rod cladding inner radius'] 

    cells['B4C CR2'] = openmc.Cell(name = 'B4C CR2')
    cells['B4C CR2'].fill = axial_materials['B4C']
    cells['B4C CR2'].region = -surfaces['BPR rod cladding inner radius']

    cells['CR moderator above core'] = openmc.Cell(name = 'CR moderator above core')
    cells['CR moderator above core'].fill = axial_materials['moderator39']
    cells['CR moderator above core'].region = +surfaces['BPR rod cladding outer radius']



    #gap
    cells['gapL'] = openmc.Cell(name='gapL')
    cells['gapL'].region = -surfaces['cladding inner radius'] & +surfaces['pin radius'] 
    cells['gapL'].fill = axial_materials['gap']

    cells['gapM'] = openmc.Cell(name='gapM')
    cells['gapM'].region = -surfaces['cladding inner radius'] & +surfaces['pin radius'] 
    cells['gapM'].fill = axial_materials['gap']

    cells['gapH'] = openmc.Cell(name='gapH')
    cells['gapH'].region = -surfaces['cladding inner radius'] & +surfaces['pin radius'] 
    cells['gapH'].fill = axial_materials['gap']

    cells['gapHBP'] = openmc.Cell(name='gapHBP')
    cells['gapHBP'].region = -surfaces['cladding inner radius'] & +surfaces['IFBA'] 
    cells['gapHBP'].fill = axial_materials['gap']
    # no fill because no need hopefullt, iff not make H2 material and fill it here

    ##cladding cells
    cells['cladBPR']= openmc.Cell(name='cladBPR')
    cells['cladBPR'].region= -surfaces['BPR rod cladding outer radius'] & +surfaces['BPR rod cladding inner radius'] 
    cells['cladBPR'].fill = axial_materials['SS304']

    cells['cladCR']= openmc.Cell(name='cladCR')
    cells['cladCR'].region= -surfaces['BPR rod cladding outer radius'] & +surfaces['BPR rod cladding inner radius'] 
    cells['cladCR'].fill = axial_materials['SS304']

    cells['cladCR2']= openmc.Cell(name='cladCR2')
    cells['cladCR2'].region= -surfaces['BPR rod cladding outer radius'] & +surfaces['BPR rod cladding inner radius'] 
    cells['cladCR2'].fill = axial_materials['SS304']

    cells['cladL']= openmc.Cell(name='cladL')
    cells['cladL'].region= -surfaces['cladding outer radius'] & +surfaces['cladding inner radius'] 
    cells['cladL'].fill = axial_materials['Cladding']

    cells['cladM']= openmc.Cell(name='cladM')
    cells['cladM'].region= -surfaces['cladding outer radius'] & +surfaces['cladding inner radius'] 
    cells['cladM'].fill = axial_materials['Cladding']

    cells['cladH']= openmc.Cell(name='cladH')
    cells['cladH'].region= -surfaces['cladding outer radius'] & +surfaces['cladding inner radius'] 
    cells['cladH'].fill = axial_materials['Cladding']

    cells['cladHBP']= openmc.Cell(name='cladHBP')
    cells['cladHBP'].region= -surfaces['cladding outer radius'] & +surfaces['cladding inner radius'] 
    cells['cladHBP'].fill = axial_materials['Cladding']

    cells['guide tube'] = openmc.Cell(name='guide tube')
    cells['guide tube'].region= +surfaces['guide inner radius'] & -surfaces['guide outer radius'] 
    cells['guide tube'].fill = axial_materials['Cladding']

    cells['guide tube BPR'] = openmc.Cell(name='guide tube BPR')
    cells['guide tube BPR'].region= +surfaces['guide inner radius'] & -surfaces['guide outer radius'] 
    cells['guide tube BPR'].fill = axial_materials['Cladding']

    cells['guide tube CR'] = openmc.Cell(name='guide tube CR')
    cells['guide tube CR'].region= +surfaces['guide inner radius'] & -surfaces['guide outer radius'] 
    cells['guide tube CR'].fill = axial_materials['Cladding']

    cells['guide tube no CR'] = openmc.Cell(name='guide tube no CR')
    cells['guide tube no CR'].region= +surfaces['guide inner radius'] & -surfaces['guide outer radius'] 
    cells['guide tube no CR'].fill = axial_materials['Cladding']

    cells['water above core'] = openmc.Cell(name='water above core')
    cells['water above core'].fill = axial_materials[f'moderator39']

    cells['water cell'] = openmc.Cell(name='water cell')
    cells['water cell'].fill = axial_materials[f'moderator20']

    cells['inconel cell'] = openmc.Cell(name='inconel cell')
    cells['inconel cell'].fill = axial_materials['SS304']

    ###Control rods

    cells['Bank A'] = openmc.Cell(name = 'Bank A')
    cells['Bank B'] = openmc.Cell(name = 'Bank B')
    cells['Bank C'] = openmc.Cell(name = 'Bank C')
    cells['Shut Down Bank'] = openmc.Cell(name = 'Shut Down Bank')

    ###Non repeated stuff
    cells['UO2L Unrodded Assembly'] = openmc.Cell(name='UO2L Unrodded Assembly')
    cells['UO2M Unrodded Assembly'] = openmc.Cell(name='UO2M Unrodded Assembly')
    cells['UO2H Unrodded Assembly'] = openmc.Cell(name='UO2H Unrodded Assembly')
    cells['UO2HBP1 Unrodded Assembly'] = openmc.Cell(name='UO2HBP1 Unrodded Assembly')
    cells['UO2HBP2 Unrodded Assembly'] = openmc.Cell(name='UO2HBP2 Unrodded Assembly')
    cells['UO2HBP2S rodded Assembly'] = openmc.Cell(name='UO2HBP2S rodded Assembly')
    cells['UO2HBP2W rodded Assembly'] = openmc.Cell(name='UO2HBP2W rodded Assembly')
    cells['UO2HBP2SW rodded Assembly'] = openmc.Cell(name='UO2HBP2SW rodded Assembly')
    cells['UO2M rodded Assembly'] = openmc.Cell(name='UO2M rodded Assembly')
    cells['UO2M Lrodded Assembly'] = openmc.Cell(name='UO2M Lrodded Assembly')
    cells['UO2M Mrodded Assembly'] = openmc.Cell(name='UO2M Mrodded Assembly')

    cells['Bank A Assembly'] = openmc.Cell( name='Bank A Assembly')
    cells['Bank B Assembly'] = openmc.Cell( name='Bank B Assembly')
    cells['Bank C Assembly'] = openmc.Cell( name='Bank C Assembly')
    cells['Bank Shut Down Assembly'] = openmc.Cell( name='Bank Shut Down Assembly')



    cells['Water Assembly'] = openmc.Cell(name='Water Assembly')
    cells['Baffle Assembly'] = openmc.Cell(name='Baffle Assembly')
    cells['Core'] = openmc.Cell(name='Core')
    cells['lower plenum']=openmc.Cell(name='lower plenum')
    cells['lower plenum'].region = +surfaces['z-min'] & -surfaces['z-bottom active'] & -surfaces['inner core barrel'] & +surfaces['qc x'] & +surfaces['qc y']

    cells['lower plenum'].fill = axial_materials['moderator0']
    cells['core barrel'] = openmc.Cell(name = 'core barrel')
    cells['core barrel'].region = -surfaces['outer core barrel'] & +surfaces['inner core barrel'] & -surfaces['z-max'] & +surfaces['z-bottom active'] & +surfaces['qc x'] & +surfaces['qc y']
    cells['core barrel'].fill = axial_materials['SS304']

    cells['core barrel replace'] = openmc.Cell(name = 'core barrel replace')
    cells['core barrel replace'].region = -surfaces['outer core barrel'] & +surfaces['inner core barrel'] & +surfaces['z-min'] & -surfaces['z-bottom active'] & +surfaces['qc x'] & +surfaces['qc y']
    cells['core barrel replace'].fill = axial_materials['moderator0']

    cells['downcomer'] = openmc.Cell(name = 'downcomer')
    cells['downcomer'].region = -surfaces['rpv inner'] & +surfaces['outer core barrel'] & -surfaces['z-max'] & +surfaces['z-min'] & +surfaces['qc x'] & +surfaces['qc y']
    cells['downcomer'].fill = axial_materials['moderator0']

    cells['rpv'] = openmc.Cell(name = 'rpv')
    cells['rpv'].region = -surfaces['rpv outer'] & +surfaces['rpv inner'] & -surfaces['z-max'] & +surfaces['z-min'] & +surfaces['qc x'] & +surfaces['qc y']
    cells['rpv'].fill = axial_materials['SS304']


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



    lattices = {}
    lattices['UO2L Unrodded Assembly'] = \
        openmc.RectLattice(name='UO2L Unrodded Assembly')
    lattices['UO2L Unrodded Assembly'].dimension = [17, 17]
    lattices['UO2L Unrodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2L Unrodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2L complete']
    g = universes['guide tube']
    lattices['UO2L Unrodded Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]


    lattices['Bank A Assembly'] = \
        openmc.RectLattice(name='Bank A Assembly')
    lattices['Bank A Assembly'].dimension = [17, 17]
    lattices['Bank A Assembly'].lower_left = [-10.71, -10.71]
    lattices['Bank A Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2L complete']
    g = universes['Bank A']
    lattices['Bank A Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]

    lattices['Bank B Assembly'] = \
        openmc.RectLattice(name='Bank B Assembly')
    lattices['Bank B Assembly'].dimension = [17, 17]
    lattices['Bank B Assembly'].lower_left = [-10.71, -10.71]
    lattices['Bank B Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2L complete']
    g = universes['Bank B']
    lattices['Bank B Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]

    lattices['Bank C Assembly'] = \
        openmc.RectLattice(name='Bank C Assembly')
    lattices['Bank C Assembly'].dimension = [17, 17]
    lattices['Bank C Assembly'].lower_left = [-10.71, -10.71]
    lattices['Bank C Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2L complete']
    g = universes['Bank C']
    lattices['Bank C Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]

    lattices['Bank Shut Down Assembly'] = \
        openmc.RectLattice(name='Bank Shut Down Assembly')
    lattices['Bank Shut Down Assembly'].dimension = [17, 17]
    lattices['Bank Shut Down Assembly'].lower_left = [-10.71, -10.71]
    lattices['Bank Shut Down Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2H complete']
    g = universes['Shut Down Bank']
    lattices['Bank Shut Down Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]



    lattices['UO2M Unrodded Assembly'] = \
        openmc.RectLattice(name='UO2M Unrodded Assembly')
    lattices['UO2M Unrodded Assembly'].dimension = [17, 17]
    lattices['UO2M Unrodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2M Unrodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2M complete']
    g = universes['guide tube w/o BPR complete']
    lattices['UO2M Unrodded Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]


    lattices['UO2H Unrodded Assembly'] = \
        openmc.RectLattice(name='UO2H Unrodded Assembly')
    lattices['UO2H Unrodded Assembly'].dimension = [17, 17]
    lattices['UO2H Unrodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2H Unrodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2H complete']
    g = universes['guide tube w/o BPR complete']
    lattices['UO2H Unrodded Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, g, u, u, u, u, u, u, u, u, u, g, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]


    lattices['UO2HBP1 Unrodded Assembly'] = \
        openmc.RectLattice(name='UO2HBP1 Unrodded Assembly')
    lattices['UO2HBP1 Unrodded Assembly'].dimension = [17, 17]
    lattices['UO2HBP1 Unrodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2HBP1 Unrodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2H complete']
    b = universes['UO2HBP complete']
    g = universes['guide tube w/o BPR complete']
    lattices['UO2HBP1 Unrodded Assembly'].universes = \
        [[b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [u, u, u, b, b, g, b, b, g, b, b, g, b, b, u, u, u],
        [u, u, b, g, u, b, u, u, b, u, u, b, u, g, b, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, g, b, b, g, b, b, g, b, b, g, b, b, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, g, b, b, g, b, b, g, b, b, g, b, b, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, g, b, b, g, b, b, g, b, b, g, b, b, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, b, g, u, b, u, u, b, u, u, b, u, g, b, u, u],
        [u, u, u, b, b, g, b, b, g, b, b, g, b, b, u, u, u],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b]]


    lattices['UO2HBP2 Unrodded Assembly'] = \
        openmc.RectLattice(name='UO2HBP2 Unrodded Assembly')
    lattices['UO2HBP2 Unrodded Assembly'].dimension = [17, 17]
    lattices['UO2HBP2 Unrodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2HBP2 Unrodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2H complete']
    b = universes['UO2HBP complete']
    g = universes['guide tube w/o BPR complete']
    lattices['UO2HBP2 Unrodded Assembly'].universes = \
        [[b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [u, u, u, b, b, g, u, b, g, b, u, g, b, b, u, u, u],
        [u, u, b, g, u, u, u, u, u, u, u, u, u, g, b, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, g, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, g, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, b, g, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, b, g, u, u, u, u, u, u, u, u, u, g, b, u, u],
        [u, u, u, b, b, g, u, b, g, b, u, g, b, b, u, u, u],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b]]



    lattices['UO2HBP2S rodded Assembly'] = \
        openmc.RectLattice(name='UO2HBP2S rodded Assembly')
    lattices['UO2HBP2S rodded Assembly'].dimension = [17, 17]
    lattices['UO2HBP2S rodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2HBP2S rodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2H complete']
    b = universes['UO2HBP complete']
    gt = universes['guide tube w BPR complete']
    g = universes['guide tube w/o BPR complete']
    lattices['UO2HBP2S rodded Assembly'].universes = \
        [[b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [u, u, u, b, b, g, u, b, g, b, u, g, b, b, u, u, u],
        [u, u, b, g, u, u, u, u, u, u, u, u, u, g, b, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, g, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, g, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, b, g, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, b, gt, u, u, u, u, u, u, u, u, u, gt, b, u, u],
        [u, u, u, b, b, gt, u, b, gt, b, u, gt, b, b, u, u, u],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b]]

    lattices['UO2HBP2W rodded Assembly'] = \
        openmc.RectLattice(name='UO2HBP2W rodded Assembly')
    lattices['UO2HBP2W rodded Assembly'].dimension = [17, 17]
    lattices['UO2HBP2W rodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2HBP2W rodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2H complete']
    b = universes['UO2HBP complete']
    gt = universes['guide tube w BPR complete']
    g = universes['guide tube w/o BPR complete']
    lattices['UO2HBP2W rodded Assembly'].universes = \
        [[b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [u, u, u, b, b, g, u, b, g, b, u, g, b, b, u, u, u],
        [u, u, b, gt, u, u, u, u, u, u, u, u, u, g, b, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, gt, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, gt, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, b, gt, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, b, gt, u, u, u, u, u, u, u, u, u, g, b, u, u],
        [u, u, u, b, b, g, u, b, g, b, u, g, b, b, u, u, u],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b]]



    #24cr
    lattices['UO2M rodded Assembly'] = \
        openmc.RectLattice(name='UO2M rodded Assembly')
    lattices['UO2M rodded Assembly'].dimension = [17, 17]
    lattices['UO2M rodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2M rodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2M complete']
    g = universes['guide tube w BPR complete']
    gt = universes['guide tube w/o BPR complete']
    lattices['UO2M rodded Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, gt, u, u, u, u, u, u, u, u, u, gt, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, gt, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, g, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, gt, u, u, u, u, u, u, u, u, u, gt, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]

    #16 cr
    lattices['UO2M Mrodded Assembly'] = \
        openmc.RectLattice(name='UO2M Mrodded Assembly')
    lattices['UO2M Mrodded Assembly'].dimension = [17, 17]
    lattices['UO2M Mrodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2M Mrodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2M complete']
    g = universes['guide tube w BPR complete']
    gt = universes['guide tube w/o BPR complete']
    lattices['UO2M Mrodded Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, gt, u, u, u, u, u, u, u, u, u, gt, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, gt, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, gt, u, u, gt, u, u, gt, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, g, u, u, gt, u, u, g, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, gt, u, u, u, u, u, u, u, u, u, gt, u, u, u],
        [u, u, u, u, u, g, u, u, g, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]

    ##12 cr inserted
    lattices['UO2M Lrodded Assembly'] = \
        openmc.RectLattice(name='UO2M Lrodded Assembly')
    lattices['UO2M Lrodded Assembly'].dimension = [17, 17]
    lattices['UO2M Lrodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2M Lrodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2M complete']
    g = universes['guide tube w BPR complete']
    gt = universes['guide tube w/o BPR complete']
    lattices['UO2M Lrodded Assembly'].universes = \
        [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, g, u, u, gt, u, u, g, u, u, u, u, u],
        [u, u, u, gt, u, u, u, u, u, u, u, u, u, gt, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, gt, u, u, g, u, u, gt, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, gt, u, u, g, u, u, gt, u, u, g, u, u, gt, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, g, u, u, gt, u, u, g, u, u, gt, u, u, g, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, gt, u, u, u, u, u, u, u, u, u, gt, u, u, u],
        [u, u, u, u, u, g, u, u, gt, u, u, g, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]



    lattices['UO2HBP2SW rodded Assembly'] = \
        openmc.RectLattice(name='UO2HBP2SW rodded Assembly')
    lattices['UO2HBP2SW rodded Assembly'].dimension = [17, 17]
    lattices['UO2HBP2SW rodded Assembly'].lower_left = [-10.71, -10.71]
    lattices['UO2HBP2SW rodded Assembly'].pitch = [1.26, 1.26]
    u = universes['UO2H complete']
    b = universes['UO2HBP complete']
    gt = universes['guide tube w BPR complete']
    g = universes['guide tube w/o BPR complete']
    lattices['UO2HBP2SW rodded Assembly'].universes = \
        [[b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [u, u, u, b, b, g, u, b, g, b, u, g, b, b, u, u, u],
        [u, u, b, g, u, u, u, u, u, u, u, u, u, g, b, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, gt, u, b, g, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, b, gt, u, b, gt, u, b, g, b, u, g, b, u, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
        [u, b, gt, u, b, gt, u, b, gt, b, u, g, b, u, g, b, u],
        [u, u, b, u, u, b, u, u, b, u, u, b, u, u, b, u, u],
        [u, u, b, gt, u, u, u, u, u, u, u, u, u, g, b, u, u],
        [u, u, u, b, b, gt, u, b, gt, b, u, gt, b, b, u, u, u],
        [b, u, u, u, u, b, u, u, b, u, u, b, u, u, u, u, b],
        [b, b, u, u, u, u, u, u, u, u, u, u, u, u, u, b, b]]



    lattices['Water Assembly'] = \
        openmc.RectLattice(name='Water Assembly')
    lattices['Water Assembly'].dimension = [1, 1]
    lattices['Water Assembly'].lower_left = [-10.71, -10.71]
    lattices['Water Assembly'].pitch = [21.42, 21.42]
    w = universes['water cell']
    lattices['Water Assembly'].universes = [[w]]


    lattices['Baffle assembly'] = \
        openmc.RectLattice(name='Baffle assembly')
    lattices['Baffle assembly'].dimension = [17, 17]
    lattices['Baffle assembly'].lower_left = [-10.71, -10.71]
    lattices['Baffle assembly'].pitch = [1.26, 1.26]
    u = universes['inconel cell']
    b = universes['water cell']
    lattices['Baffle assembly'].universes = \
    [[u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, u],
    [u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u, u]]





    cells['UO2L Unrodded Assembly'].fill = lattices['UO2L Unrodded Assembly']
    cells['UO2M Unrodded Assembly'].fill = lattices['UO2M Unrodded Assembly']
    cells['UO2H Unrodded Assembly'].fill = lattices['UO2H Unrodded Assembly']
    cells['UO2HBP1 Unrodded Assembly'].fill = lattices['UO2HBP1 Unrodded Assembly']
    cells['UO2HBP2 Unrodded Assembly'].fill = lattices['UO2HBP2 Unrodded Assembly']

    cells['UO2M rodded Assembly'].fill = lattices['UO2M rodded Assembly']
    cells['UO2M Lrodded Assembly'].fill = lattices['UO2M Lrodded Assembly']
    cells['UO2M Mrodded Assembly'].fill = lattices['UO2M Mrodded Assembly']

    cells['UO2HBP2S rodded Assembly'].fill = lattices['UO2HBP2S rodded Assembly']
    cells['UO2HBP2W rodded Assembly'].fill = lattices['UO2HBP2W rodded Assembly']
    cells['UO2HBP2SW rodded Assembly'].fill = lattices['UO2HBP2SW rodded Assembly']

    cells['Bank A Assembly'].fill = lattices['Bank A Assembly']
    cells['Bank B Assembly'].fill = lattices['Bank B Assembly']
    cells['Bank C Assembly'].fill = lattices['Bank C Assembly']
    cells['Bank Shut Down Assembly'].fill = lattices['Bank Shut Down Assembly']

    cells['Water Assembly'].fill = lattices['Water Assembly']
    cells['Baffle Assembly'].fill = lattices['Baffle assembly']





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

    cells['Core'].region = (-surfaces['inner core barrel'] & 
                            -surfaces['z-max'] & 
                            +surfaces['z-bottom active'] & 
                            +surfaces['qc x'] & 
                            +surfaces['qc y'])

    lattices['Core'] = openmc.RectLattice(name='7X7 core lattice')
    lattices['Core'].dimension = [7, 7]
    lattices['Core'].lower_left = [-w_ass/2, -w_ass/2]
    lattices['Core'].pitch = [w_ass, w_ass]

    # Define assembly types
    m = universes['Baffle Assembly']
    L = universes['UO2L Unrodded Assembly']
    M = universes['UO2M Unrodded Assembly']
    h = universes['UO2H Unrodded Assembly']
    H = universes['UO2HBP1 Unrodded Assembly']
    C = universes['UO2HBP2 Unrodded Assembly']
    I = universes['UO2M rodded Assembly']
    P = universes['UO2M Lrodded Assembly']
    G = universes['UO2M Mrodded Assembly']
    S = universes['UO2HBP2S rodded Assembly']
    W = universes['UO2HBP2W rodded Assembly']
    D = universes['UO2HBP2SW rodded Assembly']
    a = universes['Bank A Assembly']
    b = universes['Bank B Assembly']
    c = universes['Bank C Assembly']
    d = universes['Bank Shut Down Assembly']

    # Core loading pattern
    lattices['Core'].universes = [
        [m, m, m, m, m, m, m],
        [H, H, C, m, m, m, m],
        [c, P, D, d, m, m, m],
        [G, c, P, P, d, m, m],
        [b, G, c, P, D, C, m],
        [G, a, G, c, P, H, m],
        [c, G, b, G, c, H, m]
    ]

    cells['Core'].fill = lattices['Core']
    universes['Core'] = openmc.Universe(name='Core', cells=[cells['Core']])
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
    #used_surfaces = geometry.get_all_surfaces()
    #print(used_surfaces)
    # Step 2: find all defined surfaces that are not used
    #unused_surfaces = [surf for surf in surfaces.values() if surf not in used_surfaces]


    plot_1 = openmc.Plot()
    plot_1.filename = 'plot_blue_water'
    plot_1.width = [r_rpvouter, r_rpvouter] #[r_rpvouter, r_rpvouter]
    plot_1.pixels = [4000, 4000]
    plot_1.origin = [r_rpvouter/2,r_rpvouter/2,150] #[r_rpvouter/2,r_rpvouter/2,10]
    plot_1.basis = 'xy'
    plot_1.color_by = 'material'
    plot_1.colors = material_colors

    plot_2 = openmc.Plot()
    plot_2.filename = 'plot_blue_water_w_spacers2'
    plot_2.width = [r_rpvouter, r_rpvouter] #[r_rpvouter, r_rpvouter]
    plot_2.pixels = [4000, 4000]
    plot_2.origin = [r_rpvouter/2,r_rpvouter/2,-99]#[r_rpvouter/2,r_rpvouter/2,-99]
    plot_2.basis = 'xy'
    plot_2.color_by = 'material'
    plot_2.colors = material_colors

    plot_file = openmc.Plots([plot_1,plot_2])
    plot_file.export_to_xml()
    openmc.plot_geometry()

    lower_left = (0, 0, z_min)
    upper_right = (hw, hw, z_max)
    vol_calc = openmc.VolumeCalculation(list(axial_materials.values()), 100000000,
                                        lower_left, upper_right)

    settings= openmc.Settings()
    settings.batches=Batches
    settings.inactive=inactive
    settings.particles=PPB
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

    settings.source = source
    settings.volume_calculations = [vol_calc]
    settings.export_to_xml()

    tallies_file = openmc.Tallies(tallies.values())
    tallies_file.export_to_xml()
    openmc.run()
    sp = openmc.StatePoint(f'statepoint.{Batches}.h5')

    K = sp.keff
    print(sp.summary)

    """xyslice(Batches,20)
    xzslice(Batches,1)
    ppf(Batches,20)"""
    return 

run_model(
    A_Bank=0.0,
    B_Bank=0.0,
    C_Bank=0.0,
    Shut_Down_Bank=0.0,
    Batches=1000,
    PPB=1000,
    inactive=50,
    Boron_PPM=2250
    )