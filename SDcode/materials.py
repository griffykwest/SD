import openmc
import openmc.mgxs
import numpy as np
from densitylookup import *

## Starts off with regular material definitions for things
multiplier = 1.05
##UO2 low enriched
uo2l=openmc.Material()
uo2l.name='UO2L'
lenrichment=2.25*multiplier
uo2l.add_element('U',1.0,enrichment=lenrichment)
uo2l.add_element('O',2.0)
uo2l.set_density('g/cm3',10.15) #****


##UO2 medium enriched
uo2m=openmc.Material()
uo2m.name='UO2M'
menrichment=3.5*multiplier
uo2m.add_element('U',1.0,enrichment=menrichment)
uo2m.add_element('O',2.0)
uo2m.set_density('g/cm3',10.15) #****


###UO2 High enriched
uo2h=openmc.Material()
uo2h.name='UO2H'
henrichment=4.75*multiplier
uo2h.add_element('U',1.0,enrichment=henrichment)
uo2h.add_element('O',2.0)
uo2h.set_density('g/cm3',10.15) #****

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

clad=openmc.Material()
clad.name='Cladding'
clad.add_element('Sn',1.45,'wo')
clad.add_element('Fe',0.21,'wo')
clad.add_element('Cr',0.1,'wo')
clad.add_element('Zr',98.115,'wo')
clad.add_element('O',0.125,'wo')
clad.set_density('g/cm3',6.56)

##Water

ppm_Boron=2900
watertempc = 305
density = 1/pl('T',watertempc, 'vol_f')
density = density/1000

water = openmc.Material()
water.name= 'Water'
water.add_element('H', 2.0)
water.add_element('O', 1.0)
water.set_density('g/cm3', density) ## add thing so it takes a temp input and givves water density

water.add_element('B', ppm_Boron * 1e-6) ##either 

##inconel $ for lower gridshttps://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-718.pdf

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

borosilicate = openmc.Material(name='Borosilicate Glass')
borosilicate.set_density('g/cm3', 2.23)
B10 = B10enrichment*0.04
B11 = (1-B10enrichment)*0.04
borosilicate.add_nuclide('B10', B10, percent_type='wo')
borosilicate.add_nuclide('B11', B11, percent_type='wo')

# Rest of the glass (fixed)
#borosilicate.add_element('B', 0.04, percent_type='wo')
borosilicate.add_element('O',  0.535, percent_type='wo')
borosilicate.add_element('Si', 0.377, percent_type='wo')
borosilicate.add_element('Na', 0.030, percent_type='wo')
borosilicate.add_element('Al', 0.012, percent_type='wo')

gap = openmc.Material(name='gap')
gap.add_element('He', 1.0)
gap.set_density('g/cm3', 0.001)


materials = {}
materials['water'] = water
materials['UO2L']  = uo2l
materials['UO2M']  = uo2m
materials['UO2H' ] = uo2h
materials['IFBA'] = IFBA
materials['boron rod'] = borosilicate
materials['clad'] = clad
materials['SS304'] = ss304
materials['Inconel'] = inconel
materials['gap'] = gap

#print(materials)