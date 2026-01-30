import openmc

## making just the surfaces, so I need inner and outer radius for fuel, pitch, total boundaries, heights
surfaces = {}

## for fuel rods
R_f=0.82/2
surfaces['pin radius'] = openmc.ZCylinder(r=R_f, name= 'pin radius')

#IFBA inspired coating
R_IFBA=R_f+0.001 ##10 microns
surfaces['IFBA'] = openmc.ZCylinder(r=R_IFBA, name= 'IFBA')

R_ci=0.84/2
R_co=0.95/2
surfaces['cladding inner radius'] = openmc.ZCylinder(r=R_ci, name= 'cladding inner radius')
surfaces['cladding outer radius']= openmc.ZCylinder(r=R_co, name= 'cladding outer radius')

#guide tube 
R_gi=1.0/2
R_go=1.1/2
surfaces['guide inner radius'] = openmc.ZCylinder(r=R_gi, name= 'guide inner radius')
surfaces['guide outer radius']= openmc.ZCylinder(r=R_go, name= 'guide outer radius')

#BPRrod cladding
R_BPRci=0.87/2
R_BPRco=0.96/2
surfaces['BPR rod cladding inner radius'] = openmc.ZCylinder(r=R_BPRci, name= 'BPR rod cladding inner radius')
surfaces['BPR rod cladding outer radius']= openmc.ZCylinder(r=R_BPRco, name= 'BPR rod cladding outer radius')

#BPR rod absorber section
surfaces['BPR rod pin radius'] = openmc.ZCylinder(r=R_BPRci, name= 'BPR rod pin radius')

pitch=1.26

hp = pitch / 2.0
t_spacer = 0.03
surfaces['spacer x-min'] = openmc.XPlane(x0=-hp+t_spacer, name='spacer x-min')
surfaces['spacer x-max'] = openmc.XPlane(x0= hp-t_spacer, name='spacer x-max')
surfaces['spacer y-min'] = openmc.YPlane(y0=-hp+t_spacer, name='spacer y-min')
surfaces['spacer y-max'] = openmc.YPlane(y0= hp-t_spacer, name='spacer y-max')

spacer_box = (
    -surfaces['spacer x-max']
  & +surfaces['spacer x-min']
  & -surfaces['spacer y-max']
  & +surfaces['spacer y-min']
)

surfaces['outer spacer x-min'] = openmc.XPlane(x0=-hp, name='outer spacer x-min')
surfaces['outer spacer x-max'] = openmc.XPlane(x0= hp, name='outer spacer x-max')
surfaces['outer spacer y-min'] = openmc.YPlane(y0=-hp, name='outer spacer y-min')
surfaces['outer spacer y-max'] = openmc.YPlane(y0= hp, name='outer spacer y-max')

outer_spacer_box = (
    -surfaces['outer spacer x-max']
  & +surfaces['outer spacer x-min']
  & -surfaces['outer spacer y-max']
  & +surfaces['outer spacer y-min']
)
spacer_metal_region = outer_spacer_box & ~spacer_box

w_ass=17*pitch
w_core=13
w=w_core*w_ass
hw=w/2
surfaces['x-min'] = openmc.XPlane(x0=-hw, name='x-min')
surfaces['x-max'] = openmc.XPlane(x0= hw, name='x-max')
surfaces['y-min'] = openmc.YPlane(y0=-hw, name='y-min')
surfaces['y-max'] = openmc.YPlane(y0= hw, name='y-max')




#================================================
# Z in core
#================================================
z_ta=143.84
z_ba=-100
#Top of the Active fuel region
surfaces['z-top active'] = openmc.ZPlane(z0=z_ta, name='z-top active')
surfaces['z-bottom active'] = openmc.ZPlane(z0=z_ba, name='z-bottom active')


z_min=-150
z_max=z_ta+(z_ta-z_ba)
surfaces['z-min'] = openmc.ZPlane(z0=z_min)
surfaces['z-max'] = openmc.ZPlane(z0=z_max)

surfaces['x-max'].boundary_type       = 'vacuum' #The right sideand top are vacuum because they just go
surfaces['y-max'].boundary_type       = 'vacuum'

surfaces['y-min'].boundary_type       = 'vacuum' # these are reflective because of quater cre geom
surfaces['x-min'].boundary_type       = 'vacuum'

surfaces['z-min'].boundary_type       = 'vacuum' 
surfaces['z-max'].boundary_type       = 'vacuum'

#Spacer planes

"""#Top spacer
z_s3t=((z_ta-z_ba)/4)*3-z_ta+l_spacer/2 
z_s3b=z_s3t-l_spacer
surfaces['zs3t'] = openmc.ZPlane(z0=z_s3t, name='zs3t')
surfaces['zs3b'] = openmc.ZPlane(z0=z_s3b, name='zs3b')
#middle spacer
z_s2t=((z_ta-z_ba)/4)*2-z_ta+l_spacer/2 
z_s2b=z_s2t-l_spacer
surfaces['zs2t'] = openmc.ZPlane(z0=z_s2t, name='zs2t')
surfaces['zs2b'] = openmc.ZPlane(z0=z_s2b, name='zs2b')
#bottom spacer
z_s1t=((z_ta-z_ba)/4)*1-z_ta+l_spacer/2 
z_s1b=z_s1t-l_spacer
surfaces['zs1t'] = openmc.ZPlane(z0=z_s1t, name='zs1t')
surfaces['zs1b'] = openmc.ZPlane(z0=z_s1b, name='zs1b')

#Top of fuel assembly
z_tass=z_ta+15
z_bass=z_ba-10
surfaces['ztass'] = openmc.ZPlane(z0=z_tass, name='ztass')
surfaces['zbass'] = openmc.ZPlane(z0=z_bass, name='zbass')"""



##CORE BARREL STUFF
r_core = 6.15*w_ass
surfaces['inner core barrel'] = openmc.ZCylinder(r = r_core, name = 'inner core barrel')
#surfaces['inner core barrel'].boundary_type = 'vacuum'

r_corebarrel = r_core+2.54
surfaces['outer core barrel'] = openmc.ZCylinder(r = r_corebarrel, name = 'outer core barrel')
#surfaces['outer core barrel'].boundary_type = 'vacuum'

r_rpvinner= r_corebarrel+10
r_rpvouter = r_rpvinner +15

surfaces['rpv inner']= openmc.openmc.ZCylinder(r = r_rpvinner, name = 'rpv inner')
surfaces['rpv outer']= openmc.openmc.ZCylinder(r = r_rpvouter, name = 'rpv outer')
surfaces['rpv outer'].boundary_type = 'vacuum'
#print(surfaces)

### BAFFLE SURFACES ###
cedge = hw - w_ass

surfaces['baffel south'] = openmc.XPlane(x0=-cedge, name='baffle south')
surfaces['baffel north'] = openmc.XPlane(x0=cedge, name='baffle north')

surfaces['baffel east'] = openmc.YPlane(y0=-cedge, name='baffle east')
surfaces['baffel west'] = openmc.YPlane(y0=cedge, name='baffle west')


surfaces['qc x'] = openmc.XPlane(x0=0,name='qc x')
surfaces['qc y'] = openmc.YPlane(y0=0,name='qc y')

surfaces['qc x'].boundary_type = 'reflective'
surfaces['qc y'].boundary_type = 'reflective'

