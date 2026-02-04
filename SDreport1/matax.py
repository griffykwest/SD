import openmc
import numpy as np
from densitylookup import *
from surfaces import *
from specialinputs import*



# ----------------------------
# Axial parameters
# ----------------------------
n_axial = 40                # number of axial slices
z_bot =  z_ba               # bottom of active fuel
z_top = z_ta          # top of active fuel (m)
z_edges = np.linspace(z_bot, z_top, n_axial + 1)
z_centers = 0.5 * (z_edges[:-1] + z_edges[1:])

z_upper_edges = z_edges +z_top-z_bot

z_cr_edges = np.concatenate((z_edges[0:n_axial], z_upper_edges))
#print(z_cr_edges[40])
h = np.linspace(0, 1, n_axial)  # normalized axial position 0->1

T_min = 368
T_max = 756

T_avg = (T_max + T_min) / 2
T_amp = T_max-T_min

# Cosine shape, peak in the middle, edges at min
T_fuel_z = T_min + T_amp * np.cos(np.pi * (h - 0.5))
#print(T_fuel_z)

T_mod_z  = np.linspace(T_mod_min+273.15, T_mod_max+273.15, n_axial)


axial_materials = {}
multiplier = 0.95
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
B10_enr = 0.25 # for coating
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
inconel.add_element("Ni", 51.19/100, percent_type="wo")
inconel.add_element("Cr", 18.96/100, percent_type="wo")
#inconel.add_element("Nb", 5.0/100, percent_type="wo")
#inconel.add_element("Mo", 3.0/100, percent_type="wo")
#inconel.add_element("Ti", 0.75/100, percent_type="wo")
#inconel.add_element("Al", 0.4/100, percent_type="wo")
#inconel.add_element("Co", 0.5/100, percent_type="wo")
inconel.add_element("Mn", 0.87/100, percent_type="wo")
inconel.add_element("Si", 0.35/100, percent_type="wo")
#inconel.add_element("P",  0.0075/100, percent_type="wo")
#inconel.add_element("S",  0.0075/100, percent_type="wo")
#inconel.add_element("C",  0.15/100, percent_type="wo")
inconel.add_element("Fe", 28.63/100, percent_type="wo")

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
#MAterials from https://github.com/ukaea/neutronics_material_maker/blob/main/neutronics_material_maker/data/pnnl_materials.json

## from source
BSG = openmc.Material(name='BSG')

# Typical borosilicate glass density
BSG.set_density('g/cm3', 2.23)

BSG.add_nuclide('B10', 0.699, 'wo')
BSG.add_nuclide('B11', 3.207, 'wo')
BSG.add_element('O',  53.902, 'wo')
BSG.add_element('Si', 37.586, 'wo')
BSG.add_element('K',   0.332, 'wo')
BSG.add_element('Na',  2.837, 'wo')

Al2O3_B4C = openmc.Material(name='Al2O3-B4C')

# Reasonable effective density for Al2O3-dominated composite
Al2O3_B4C.set_density('g/cm3', 2.593)

Al2O3_B4C.add_nuclide('B10', 1.968, 'wo')
Al2O3_B4C.add_nuclide('B11', 8.992, 'wo')
Al2O3_B4C.add_element('C',  3.040, 'wo')
Al2O3_B4C.add_element('O', 40.479, 'wo')
Al2O3_B4C.add_element('Al',45.521, 'wo')



B10enrichmentB4C = 0.85  # 20% B-10, adjust as needed
B4C = openmc.Material(name='Boron Carbide (B4C)')
B4C.set_density('g/cm3', 2.52)

B_total = 0.799981

B4C.add_nuclide('B10', B_total * B10enrichmentB4C, percent_type='ao')
B4C.add_nuclide('B11', B_total * (1.0 - B10enrichmentB4C), percent_type='ao')
B4C.add_element('C', 0.200019, percent_type='ao')

Ag_In_Cd = openmc.Material(name= 'Ag_In_Cd')
Ag_In_Cd.add_element('Ag', 0.8)
Ag_In_Cd.add_element('In', 0.15)
Ag_In_Cd.add_element('Cd', 0.05)
Ag_In_Cd.set_density('g/cm3', 10.16)

gap = openmc.Material(name='gap')
gap.add_element('He', 1.0)
gap.set_density('g/cm3', 0.001)

axial_materials['IFBA'] = IFBA
axial_materials['BSG'] = BSG 
axial_materials['Al2O3_B4C'] = Al2O3_B4C
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

        axial_cells[f'spacer{i}'] = openmc.Cell(name= f'spacer{i}', fill = axial_materials['Cladding'], region= spacer_region)
        axial_cells[f'g spacer{i}'] = openmc.Cell(name= f'g spacer{i}', fill = axial_materials['Cladding'], region=spacer_region)
    else:
        axial_cells[f'moderator{i}'] = openmc.Cell(name = f'moderator{i}', fill= axial_materials[f'moderator{i}'], region=+surfaces['cladding outer radius'] & z_bottom & z_top)
        axial_cells[f'moderator{i}'].temperature = axial_materials[f'moderator{i}'].temperature

        axial_cells[f'guide moderator{i}'] = openmc.Cell(name = f'guide moderator{i}', fill= axial_materials[f'moderator{i}'], region=+surfaces['guide outer radius'] & z_bottom & z_top)
        axial_cells[f'guide moderator{i}'].temperature = axial_materials[f'moderator{i}'].temperature


    axial_cells[f'inner guide moderator no BPR{i}'] = openmc.Cell(name = f'inner guide moderator no BPR{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['guide inner radius'] & z_bottom & z_top)
    axial_cells[f'inner guide moderator no BPR{i}'].temperature = axial_materials[f'moderator{i}'].temperature

    axial_cells[f'inner guide moderator w BPR{i}'] = openmc.Cell(name = f'inner guide moderator w BPR{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['guide inner radius'] & +surfaces['BSG rod cladding outer radius'] & z_bottom & z_top)
    axial_cells[f'inner guide moderator w BPR{i}'].temperature = axial_materials[f'moderator{i}'].temperature   
    
    axial_cells[f'inner inner guide moderator w Al2O3_B4C{i}'] = openmc.Cell(name = f'inner inner guide moderator w Al2O3_B4C{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['AlB4C inner rod cladding inner radius'] & z_bottom & z_top)
    axial_cells[f'inner inner guide moderator w Al2O3_B4C{i}'].temperature = axial_materials[f'moderator{i}'].temperature
    
    axial_cells[f'inner inner guide moderator w BSG{i}'] = openmc.Cell(name = f'inner inner guide moderator w BSG{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['BSG inner rod cladding inner radius'] & z_bottom & z_top)
    axial_cells[f'inner inner guide moderator w BSG{i}'].temperature = axial_materials[f'moderator{i}'].temperature

    axial_cells[f'inner guide moderator no CR{i}'] = openmc.Cell(name = f'inner guide moderator no CR{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['guide inner radius'] & z_bottom & z_top)
    axial_cells[f'inner guide moderator no CR{i}'].temperature = axial_materials[f'moderator{i}'].temperature

    axial_cells[f'inner guide moderator w CR{i}'] = openmc.Cell(name = f'inner guide moderator w CR{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['CR rod cladding inner radius'] & z_bottom & z_top)
    axial_cells[f'inner guide moderator w CR{i}'].temperature = axial_materials[f'moderator{i}'].temperature   
    
    


uo2l_axial_cells = []
uo2m_axial_cells = []
uo2h_axial_cells = []
spacer_axial_cells = []
moderator_axial_cells = []
g_moderator_axial_cells = []
i_g_moderator_axial_cells_n_BPR = []
i_g_moderator_axial_cells_w_BPR = []
i_i_g_moderator_axial_cells_w_Al2O3_B4C = []
i_i_g_moderator_axial_cells_w_BSG = []
i_g_moderator_axial_cells_n_CR = []
i_g_moderator_axial_cells_w_CR = []


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
    i_i_g_moderator_axial_cells_w_BSG.append(axial_cells[f'inner inner guide moderator w BSG{i}'])
    i_i_g_moderator_axial_cells_w_Al2O3_B4C.append(axial_cells[f'inner inner guide moderator w Al2O3_B4C{i}'])
    i_g_moderator_axial_cells_n_CR.append(axial_cells[f'inner guide moderator no CR{i}'])
    i_g_moderator_axial_cells_w_CR.append(axial_cells[f'inner guide moderator w CR{i}'])



UO2L_cont_universe = openmc.Universe(cells=uo2l_axial_cells)
UO2M_cont_universe = openmc.Universe(cells=uo2m_axial_cells)
UO2H_cont_universe = openmc.Universe(cells=uo2h_axial_cells)
moderator_cont_universe = openmc.Universe(cells=moderator_axial_cells)

g_moderator_cont_universe = openmc.Universe(cells=g_moderator_axial_cells)
i_g_moderator_n_BPR_cont_universe = openmc.Universe(cells=i_g_moderator_axial_cells_n_BPR)
i_g_moderator_w_BPR_cont_universe = openmc.Universe(cells=i_g_moderator_axial_cells_w_BPR)
i_i_g_moderator_w_BSG_cont_universe = openmc.Universe(cells=i_i_g_moderator_axial_cells_w_BSG)
i_i_g_moderator_w_Al2O3_B4C_cont_universe = openmc.Universe(cells=i_i_g_moderator_axial_cells_w_Al2O3_B4C)
i_g_moderator_n_CR_cont_universe = openmc.Universe(cells=i_g_moderator_axial_cells_n_CR)
i_g_moderator_w_CR_cont_universe = openmc.Universe(cells=i_g_moderator_axial_cells_w_CR)
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
cells['g_moderator5'] = openmc.Cell(name='g_moderator5', region = +surfaces['guide outer radius'], fill = g_moderator_cont_universe)
cells['inner guide moderator no CR'] = openmc.Cell(name='inner guide moderator no CR', region = -surfaces['guide inner radius'], fill = i_g_moderator_n_CR_cont_universe)
cells['inner guide moderator no BPR'] = openmc.Cell(name='inner guide moderator no BPR', region = -surfaces['guide inner radius'], fill = i_g_moderator_n_BPR_cont_universe)
cells['inner guide moderator w BSG'] = openmc.Cell(name='inner guide moderator w BSG', region = -surfaces['guide inner radius'] & +surfaces['BSG rod cladding outer radius'], fill = i_g_moderator_w_BPR_cont_universe)
cells['inner guide moderator w Al2O3_B4C'] = openmc.Cell(name='inner guide moderator w Al2O3_B4C', region = -surfaces['guide inner radius'] & +surfaces['AlB4C rod cladding outer radius'], fill = i_g_moderator_w_BPR_cont_universe)
cells['inner inner guide moderator w BSG'] = openmc.Cell(name='inner inner guide moderator w BSG', region = -surfaces['BSG inner rod cladding inner radius'], fill = i_i_g_moderator_w_BSG_cont_universe)
cells['inner inner guide moderator w Al2O3_B4C'] = openmc.Cell(name='inner inner guide moderator w Al2O3_B4C', region = -surfaces['AlB4C inner rod cladding inner radius'], fill = i_i_g_moderator_w_Al2O3_B4C_cont_universe)
cells['inner guide moderator w CR'] = openmc.Cell(name='inner guide moderator w CR', region = -surfaces['guide inner radius'] & +surfaces['CR rod cladding outer radius'], fill = i_g_moderator_w_CR_cont_universe)

"""#print(cells['spacerL'])
#print(cells['UO2L'])
#print(cells['moderatorHBP'])"""

#IFBA coating on high enriched
cells['IFBA'] = openmc.Cell(name='IFBA')
cells['IFBA'].region = -surfaces['IFBA'] & +surfaces['pin radius'] 
cells['IFBA'].fill = axial_materials['IFBA']

#Integral control rod
cells['Al2O3_B4C'] = openmc.Cell(name = 'Al2O3_B4C')
cells['Al2O3_B4C'].fill = axial_materials['Al2O3_B4C']
cells['Al2O3_B4C'].region = -surfaces['AlB4C rod outer radius'] & +surfaces['AlB4C rod inner radius']

cells['Al2O3_B4C Outer Gap'] = openmc.Cell(name = 'Al2O3_B4C Outer Gap')
cells['Al2O3_B4C Outer Gap'].fill = axial_materials['gap']
cells['Al2O3_B4C Outer Gap'].region = -surfaces['AlB4C rod cladding inner radius'] & +surfaces['AlB4C rod outer radius']

cells['Al2O3_B4C Inner Gap'] = openmc.Cell(name = 'Al2O3_B4C Inner Gap')
cells['Al2O3_B4C Inner Gap'].fill = axial_materials['gap']
cells['Al2O3_B4C Inner Gap'].region = -surfaces['AlB4C rod inner radius'] & +surfaces['AlB4C inner rod cladding outer radius']

cells['outer clad Al2O3_B4C']= openmc.Cell(name='outer clad Al2O3_B4C')
cells['outer clad Al2O3_B4C'].region= -surfaces['AlB4C rod cladding outer radius'] & +surfaces['AlB4C rod cladding inner radius']
cells['outer clad Al2O3_B4C'].fill = axial_materials['Cladding']

cells['inner clad Al2O3_B4C']= openmc.Cell(name='inner clad Al2O3_B4C')
cells['inner clad Al2O3_B4C'].region= -surfaces['AlB4C inner rod cladding outer radius'] & +surfaces['AlB4C inner rod cladding inner radius']
cells['inner clad Al2O3_B4C'].fill = axial_materials['Cladding']

cells['guide tube Al2O3_B4C'] = openmc.Cell(name='guide tube Al2O3_B4C')
cells['guide tube Al2O3_B4C'].region= +surfaces['guide inner radius'] & -surfaces['guide outer radius'] 
cells['guide tube Al2O3_B4C'].fill = axial_materials['Cladding']


#Integral control rod
cells['BSG'] = openmc.Cell(name = 'BSG')
cells['BSG'].fill = axial_materials['BSG']
cells['BSG'].region = -surfaces['BSG rod outer radius'] & +surfaces['BSG rod inner radius']

cells['BSG Outer Gap'] = openmc.Cell(name = 'BSG Outer Gap')
cells['BSG Outer Gap'].fill = axial_materials['gap']
cells['BSG Outer Gap'].region = -surfaces['BSG rod cladding inner radius'] & +surfaces['BSG rod outer radius']

cells['BSG Inner Gap'] = openmc.Cell(name = 'BSG Inner Gap')
cells['BSG Inner Gap'].fill = axial_materials['gap']
cells['BSG Inner Gap'].region = -surfaces['BSG rod inner radius'] & +surfaces['BSG inner rod cladding outer radius']

cells['outer clad BSG']= openmc.Cell(name='outer clad BSG')
cells['outer clad BSG'].region= -surfaces['BSG rod cladding outer radius'] & +surfaces['BSG rod cladding inner radius']
cells['outer clad BSG'].fill = axial_materials['SS304']

cells['inner clad BSG']= openmc.Cell(name='inner clad BSG')
cells['inner clad BSG'].region= -surfaces['BSG inner rod cladding outer radius'] & +surfaces['BSG inner rod cladding inner radius']
cells['inner clad BSG'].fill = axial_materials['SS304']

cells['guide tube BSG'] = openmc.Cell(name='guide tube BSG')
cells['guide tube BSG'].region= +surfaces['guide inner radius'] & -surfaces['guide outer radius'] 
cells['guide tube BSG'].fill = axial_materials['Cladding']

"""root = openmc.Universe(cells=[cells['outer clad BSG']])
geometry = openmc.Geometry(root)
geometry.export_to_xml()

# --- Plot ---
plot = openmc.Plot()
plot.filename = 'cell_xy'
plot.origin = (0.0, 0.0, 0.0)
plot.width = (1.0, 1.0)
plot.pixels = (600, 600)
plot.color_by = 'cell'
plot.basis = 'xy'

plots = openmc.Plots([plot])
plots.export_to_xml()

openmc.plot_geometry()"""


cells['B4C CR'] = openmc.Cell(name = 'B4C CR')
cells['B4C CR'].fill = axial_materials['B4C']
cells['B4C CR'].region = -surfaces['CR rod cladding inner radius'] 

cells['B4C CR2'] = openmc.Cell(name = 'B4C CR2')
cells['B4C CR2'].fill = axial_materials['B4C']
cells['B4C CR2'].region = -surfaces['CR rod cladding inner radius']

cells['CR moderator above core'] = openmc.Cell(name = 'CR moderator above core')
cells['CR moderator above core'].fill = axial_materials['moderator39']
cells['CR moderator above core'].region = +surfaces['CR rod cladding outer radius']



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


cells['cladCR']= openmc.Cell(name='cladCR')
cells['cladCR'].region= -surfaces['CR rod cladding outer radius'] & +surfaces['CR rod cladding inner radius'] 
cells['cladCR'].fill = axial_materials['SS304']

cells['cladCR2']= openmc.Cell(name='cladCR2')
cells['cladCR2'].region= -surfaces['CR rod cladding outer radius'] & +surfaces['CR rod cladding inner radius'] 
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
cells['UO2HBP3 Unrodded Assembly'] = openmc.Cell(name='UO2HBP3 Unrodded Assembly')
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
cells['BP Bank Shut Down Assembly'] = openmc.Cell( name='BP Bank Shut Down Assembly')
cells['Low Bank Shut Down Assembly'] = openmc.Cell( name='Low Bank Shut Down Assembly')



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




##print(cells)