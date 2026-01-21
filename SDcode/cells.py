import openmc
from materials import materials
from surfaces import surfaces

cells = {}


watertempc = 305
fueltempc = 800
## for just the fuel
cells['UO2L'] = openmc.Cell(name='UO2L')
cells['UO2M'] = openmc.Cell(name='UO2M')
cells['UO2H'] = openmc.Cell(name='UO2H')
cells['UO2HBP'] = openmc.Cell(name='UO2HBP')

cells['UO2L'].region = -surfaces['pin radius']
cells['UO2M'].region = -surfaces['pin radius']
cells['UO2H'].region = -surfaces['pin radius']
cells['UO2HBP'].region = -surfaces['pin radius']

cells['UO2L'].fill = materials['UO2L']
cells['UO2M'].fill = materials['UO2M']
cells['UO2H'].fill = materials['UO2H']
cells['UO2HBP'].fill = materials['UO2H']

#IFBA coating on high enriched
cells['IFBA'] = openmc.Cell(name='IFBA')
cells['IFBA'].region = -surfaces['IFBA'] & +surfaces['pin radius']
cells['IFBA'].fill = materials['IFBA']

#Integral control rod
cells['CRboron'] = openmc.Cell(name = 'CRboron')
cells['CRboron'].fill = materials['boron rod']
cells['CRboron'].region = -surfaces['control rod cladding inner radius']

#gap
cells['gapL'] = openmc.Cell(name='gapL')
cells['gapL'].region = -surfaces['cladding inner radius'] & +surfaces['pin radius']
cells['gapL'].fill = materials['gap']

cells['gapM'] = openmc.Cell(name='gapM')
cells['gapM'].region = -surfaces['cladding inner radius'] & +surfaces['pin radius']
cells['gapM'].fill = materials['gap']

cells['gapH'] = openmc.Cell(name='gapH')
cells['gapH'].region = -surfaces['cladding inner radius'] & +surfaces['pin radius']
cells['gapH'].fill = materials['gap']

cells['gapHBP'] = openmc.Cell(name='gapHBP')
cells['gapHBP'].region = -surfaces['cladding inner radius'] & +surfaces['IFBA']
cells['gapHBP'].fill = materials['gap']
# no fill because no need hopefullt, iff not make H2 material and fill it here

##cladding cells
cells['cladCR']= openmc.Cell(name='cladCR')
cells['cladCR'].region= -surfaces['control rod cladding outer radius'] & +surfaces['control rod cladding inner radius']
cells['cladCR'].fill = materials['SS304']

cells['cladL']= openmc.Cell(name='cladL')
cells['cladL'].region= -surfaces['cladding outer radius'] & +surfaces['cladding inner radius']
cells['cladL'].fill = materials['clad']

cells['cladM']= openmc.Cell(name='cladM')
cells['cladM'].region= -surfaces['cladding outer radius'] & +surfaces['cladding inner radius']
cells['cladM'].fill = materials['clad']

cells['cladH']= openmc.Cell(name='cladH')
cells['cladH'].region= -surfaces['cladding outer radius'] & +surfaces['cladding inner radius']
cells['cladH'].fill = materials['clad']

cells['cladHBP']= openmc.Cell(name='cladHBP')
cells['cladHBP'].region= -surfaces['cladding outer radius'] & +surfaces['cladding inner radius']
cells['cladHBP'].fill = materials['clad']

cells['guide tube'] = openmc.Cell(name='guide tube')
cells['guide tube'].region= +surfaces['guide inner radius'] & -surfaces['guide outer radius']
cells['guide tube'].fill = materials['clad']

cells['guide tube CR'] = openmc.Cell(name='guide tube CR')
cells['guide tube CR'].region= +surfaces['guide inner radius'] & -surfaces['guide outer radius']
cells['guide tube CR'].fill = materials['clad']



## water around fuel rods
cells['moderatorL'] = openmc.Cell(name='moderatorL')
cells['moderatorL'].region= +surfaces['cladding outer radius']
cells['moderatorL'].fill = materials['water']

cells['moderatorM'] = openmc.Cell(name='moderatorM')
cells['moderatorM'].region= +surfaces['cladding outer radius']
cells['moderatorM'].fill = materials['water']

cells['moderatorH'] = openmc.Cell(name='moderatorH')
cells['moderatorH'].region= +surfaces['cladding outer radius']
cells['moderatorH'].fill = materials['water']

cells['moderatorHBP'] = openmc.Cell(name='moderatorHBP')
cells['moderatorHBP'].region= +surfaces['cladding outer radius']
cells['moderatorHBP'].fill = materials['water']

cells['moderatorG'] = openmc.Cell(name='moderatorG')
cells['moderatorG'].region= +surfaces['guide outer radius']
cells['moderatorG'].fill = materials['water']

cells['moderatorCR'] = openmc.Cell(name='moderatorCR')
cells['moderatorCR'].region= +surfaces['guide outer radius']
cells['moderatorCR'].fill = materials['water']


## water guide tube for empty fuel rod
cells['guide moderator'] = openmc.Cell(name='guide moderator')
cells['guide moderator'].region= -surfaces['guide inner radius']
cells['guide moderator'].fill = materials['water']

cells['guide moderator w CR'] = openmc.Cell(name='guide moderator w CR')
cells['guide moderator w CR'].region= -surfaces['guide inner radius'] & +surfaces['control rod cladding outer radius']
cells['guide moderator w CR'].fill = materials['water']

##water Cell
cells['water cell'] = openmc.Cell(name='water cell')
cells['water cell'].fill = materials['water']

cells['inconel cell'] = openmc.Cell(name='inconel cell')
cells['inconel cell'].fill = materials['Inconel']


cells['UO2L Unrodded Assembly'] = openmc.Cell(name='UO2L Unrodded Assembly')
cells['UO2M Unrodded Assembly'] = openmc.Cell(name='UO2M Unrodded Assembly')
cells['UO2H Unrodded Assembly'] = openmc.Cell(name='UO2H Unrodded Assembly')
cells['UO2HBP1 Unrodded Assembly'] = openmc.Cell(name='UO2HBP1 Unrodded Assembly')
cells['UO2HBP2 Unrodded Assembly'] = openmc.Cell(name='UO2HBP2 Unrodded Assembly')

cells['UO2HBP2E rodded Assembly'] = openmc.Cell(name='UO2HBP2E rodded Assembly')
cells['UO2HBP2S rodded Assembly'] = openmc.Cell(name='UO2HBP2S rodded Assembly')
cells['UO2HBP2W rodded Assembly'] = openmc.Cell(name='UO2HBP2W rodded Assembly')
cells['UO2HBP2N rodded Assembly'] = openmc.Cell(name='UO2HBP2N rodded Assembly')

cells['UO2HBP2NE rodded Assembly'] = openmc.Cell(name='UO2HBP2NE rodded Assembly')
cells['UO2HBP2SE rodded Assembly'] = openmc.Cell(name='UO2HBP2SE rodded Assembly')
cells['UO2HBP2SW rodded Assembly'] = openmc.Cell(name='UO2HBP2SW rodded Assembly')
cells['UO2HBP2NW rodded Assembly'] = openmc.Cell(name='UO2HBP2NW rodded Assembly')

cells['UO2M rodded Assembly'] = openmc.Cell(name='UO2M rodded Assembly')
cells['UO2M Lrodded Assembly'] = openmc.Cell(name='UO2M Lrodded Assembly')
cells['UO2M Mrodded Assembly'] = openmc.Cell(name='UO2M Mrodded Assembly')

cells['Water Assembly'] = openmc.Cell(name='Water Assembly')
cells['Baffle Assembly'] = openmc.Cell(name='Baffle Assembly')
cells['Core'] = openmc.Cell(name='Core')
cells['lower plenum']=openmc.Cell(name='lower plenum')
cells['upper plenum']=openmc.Cell(name='upper plenum')

cells['lower plenum'].region = -surfaces['z-max'] & +surfaces['z-top active'] & -surfaces['inner core barrel']
cells['upper plenum'].region = +surfaces['z-min'] & -surfaces['z-bottom active'] & -surfaces['inner core barrel']

cells['lower plenum'].fill = materials['water']
cells['upper plenum'].fill = materials['water']

cells['core barrel'] = openmc.Cell(name = 'core barrel')
cells['core barrel'].region = -surfaces['outer core barrel'] & +surfaces['inner core barrel'] & -surfaces['z-max'] & +surfaces['z-min']
cells['core barrel'].fill = materials['SS304']

cells['downcomer'] = openmc.Cell(name = 'downcomer')
cells['downcomer'].region = -surfaces['rpv inner'] & +surfaces['outer core barrel'] & -surfaces['z-max'] & +surfaces['z-min']
cells['downcomer'].fill = materials['water']

cells['rpv'] = openmc.Cell(name = 'rpv')
cells['rpv'].region = -surfaces['rpv outer'] & +surfaces['rpv inner'] & -surfaces['z-max'] & +surfaces['z-min']
cells['rpv'].fill = materials['SS304']

#print(cells)
##Temperatures

watertemp = 305+273.15
fueltemp = 700 +273.15

cells['moderatorL'].temperature = watertemp
cells['moderatorM'].temperature = watertemp
cells['moderatorH'].temperature = watertemp
cells['moderatorHBP'].temperature = watertemp
cells['moderatorG'].temperature = watertemp
cells['moderatorCR'].temperature = watertemp
cells['guide moderator'].temperature = watertemp
cells['guide moderator w CR'].temperature = watertemp
cells['water cell'].temperature = watertemp
cells['downcomer'].temperature = watertemp


cells['UO2L'].temperature = fueltemp
cells['UO2M'].temperature = fueltemp
cells['UO2H'].temperature = fueltemp
cells['UO2HBP'].temperature = fueltemp