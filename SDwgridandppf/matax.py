import openmc
import numpy as np
from densitylookup import *
from surfaces import *


# ----------------------------
# Axial parameters
# ----------------------------
n_axial = 40                # number of axial slices
z_bot = -100                 # bottom of active fuel
z_top = 143.84               # top of active fuel (m)
z_edges = np.linspace(z_bot, z_top, n_axial + 1)
z_centers = 0.5 * (z_edges[:-1] + z_edges[1:])

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
ppm_Boron=2200
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
    moderator.add_element('B', ppm_Boron * 1e-6)
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
zirc = (99.83-1.03,)/100
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

#print(axial_materials)

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


    axial_cells[f'inner guide moderator no CR{i}'] = openmc.Cell(name = f'inner guide moderator no CR{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['guide inner radius'] & z_bottom & z_top)
    axial_cells[f'inner guide moderator no CR{i}'].temperature = axial_materials[f'moderator{i}'].temperature

    axial_cells[f'inner guide moderator w CR{i}'] = openmc.Cell(name = f'inner guide moderator w CR{i}', fill= axial_materials[f'moderator{i}'], region=-surfaces['guide inner radius'] & +surfaces['control rod cladding outer radius'] & z_bottom & z_top)
    axial_cells[f'inner guide moderator w CR{i}'].temperature = axial_materials[f'moderator{i}'].temperature



uo2l_axial_cells = []
uo2m_axial_cells = []
uo2h_axial_cells = []
spacer_axial_cells = []
moderator_axial_cells = []
g_moderator_axial_cells = []
i_g_moderator_axial_cells_n_CR = []
i_g_moderator_axial_cells_w_CR = []


for i in range(n_axial):
    uo2l_axial_cells.append(axial_cells[f'UO2L{i}'])
    uo2m_axial_cells.append(axial_cells[f'UO2M{i}'])
    uo2h_axial_cells.append(axial_cells[f'UO2H{i}'])
    moderator_axial_cells.append(axial_cells[f'moderator{i}'])
    g_moderator_axial_cells.append(axial_cells[f'guide moderator{i}'])
    if i in spacer_indices:
        moderator_axial_cells.append(axial_cells[f'spacer{i}'])
        g_moderator_axial_cells.append(axial_cells[f'g spacer{i}'])
    i_g_moderator_axial_cells_n_CR.append(axial_cells[f'inner guide moderator no CR{i}'])
    i_g_moderator_axial_cells_w_CR.append(axial_cells[f'inner guide moderator w CR{i}'])

UO2L_cont_universe = openmc.Universe(cells=uo2l_axial_cells)
UO2M_cont_universe = openmc.Universe(cells=uo2m_axial_cells)
UO2H_cont_universe = openmc.Universe(cells=uo2h_axial_cells)
moderator_cont_universe = openmc.Universe(cells=moderator_axial_cells)

g_moderator_cont_universe = openmc.Universe(cells=g_moderator_axial_cells)
i_g_moderator_n_CR_cont_universe = openmc.Universe(cells=i_g_moderator_axial_cells_n_CR)
i_g_moderator_w_CR_cont_universe = openmc.Universe(cells=i_g_moderator_axial_cells_w_CR)



#print(spacer_cont_universe)
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
cells['inner guide moderator no CR'] = openmc.Cell(name='inner guide moderator no CR', region = -surfaces['guide inner radius'], fill = i_g_moderator_n_CR_cont_universe)
cells['inner guide moderator w CR'] = openmc.Cell(name='inner guide moderator w CR', region = -surfaces['guide inner radius'] & +surfaces['control rod cladding outer radius'], fill = i_g_moderator_w_CR_cont_universe)

"""print(cells['spacerL'])
print(cells['UO2L'])
print(cells['moderatorHBP'])"""

#IFBA coating on high enriched
cells['IFBA'] = openmc.Cell(name='IFBA')
cells['IFBA'].region = -surfaces['IFBA'] & +surfaces['pin radius']
cells['IFBA'].fill = axial_materials['IFBA']

#Integral control rod
cells['CRboron'] = openmc.Cell(name = 'CRboron')
cells['CRboron'].fill = axial_materials['Borosilicate Glass']
cells['CRboron'].region = -surfaces['control rod cladding inner radius']

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
cells['cladCR'].region= -surfaces['control rod cladding outer radius'] & +surfaces['control rod cladding inner radius']
cells['cladCR'].fill = axial_materials['SS304']

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

cells['water cell'] = openmc.Cell(name='water cell')
cells['water cell'].fill = axial_materials[f'moderator20']

cells['inconel cell'] = openmc.Cell(name='inconel cell')
cells['inconel cell'].fill = axial_materials['SS304']

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

cells['Water Assembly'] = openmc.Cell(name='Water Assembly')
cells['Baffle Assembly'] = openmc.Cell(name='Baffle Assembly')
cells['Core'] = openmc.Cell(name='Core')
cells['lower plenum']=openmc.Cell(name='lower plenum')
cells['upper plenum']=openmc.Cell(name='upper plenum')

cells['upper plenum'].region = -surfaces['z-max'] & +surfaces['z-top active'] & -surfaces['inner core barrel'] & +surfaces['qc x'] & +surfaces['qc y']
cells['lower plenum'].region = +surfaces['z-min'] & -surfaces['z-bottom active'] & -surfaces['inner core barrel'] & +surfaces['qc x'] & +surfaces['qc y']

cells['lower plenum'].fill = axial_materials['moderator0']
cells['upper plenum'].fill = axial_materials['moderator39']

cells['core barrel'] = openmc.Cell(name = 'core barrel')
cells['core barrel'].region = -surfaces['outer core barrel'] & +surfaces['inner core barrel'] & -surfaces['z-max'] & +surfaces['z-min'] & +surfaces['qc x'] & +surfaces['qc y']
cells['core barrel'].fill = axial_materials['SS304']

cells['downcomer'] = openmc.Cell(name = 'downcomer')
cells['downcomer'].region = -surfaces['rpv inner'] & +surfaces['outer core barrel'] & -surfaces['z-max'] & +surfaces['z-min'] & +surfaces['qc x'] & +surfaces['qc y']
cells['downcomer'].fill = axial_materials['moderator0']

cells['rpv'] = openmc.Cell(name = 'rpv')
cells['rpv'].region = -surfaces['rpv outer'] & +surfaces['rpv inner'] & -surfaces['z-max'] & +surfaces['z-min'] & +surfaces['qc x'] & +surfaces['qc y']
cells['rpv'].fill = axial_materials['SS304']

temp_universe = openmc.Universe(cells=[cells['moderatorL']])



#print(cells)