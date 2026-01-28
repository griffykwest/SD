import openmc
from newuniverses import universes, cells



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
g = universes['guide tube']
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
g = universes['guide tube']
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
g = universes['guide tube']
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


cells['Water Assembly'].fill = lattices['Water Assembly']
cells['Baffle Assembly'].fill = lattices['Baffle assembly']

