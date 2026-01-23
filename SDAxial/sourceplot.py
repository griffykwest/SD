import openmc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from surfaces import *

sp = openmc.StatePoint('statepoint.501.h5')

plt.quiver(sp.source['r']['x'], sp.source['r']['y'],
           sp.source['u']['x'], sp.source['u']['y'],
           np.log(sp.source['E']), cmap='jet', scale=2000.0)
plt.colorbar()

R = 6.04 * 21.42  # radius in cm
circle = Circle((0.0, 0.0), R, fill=False, linewidth=2)
plt.gca().add_patch(circle)

plt.xlabel('x [cm]')
plt.ylabel('y [cm]')
plt.xlim(-hw,hw)
plt.ylim(-hw,hw)
plt.gca().set_aspect('equal')
plt.savefig('sourcedist.png', dpi=1000)
plt.show()
