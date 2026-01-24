import openmc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from surfaces import *

def qtf(arr):
    x_mirror = np.flip(arr, axis=0)
    right = np.vstack([x_mirror[:-1], (x_mirror[-1] + arr[0]) / 2, arr[1:]])
    left = np.flip(right, axis=1)
    full = np.hstack([left[:, :-1], (left[:, -1:] + right[:, 0:1]) / 2, right[:, 1:]])
    return full

sp = openmc.StatePoint('statepoint.1000.h5')

plt.quiver(sp.source['r']['x'], sp.source['r']['y'],
           sp.source['u']['x'], sp.source['u']['y'],
           np.log10(sp.source['E']), cmap='jet', scale=2000.0)
plt.colorbar()

R = 6.04 * 21.42  # radius in cm
circle = Circle((0.0, 0.0), R, fill=False, linewidth=2)
plt.gca().add_patch(circle)

plt.xlabel('x [cm]')
plt.ylabel('y [cm]')
plt.xlim(0,hw)
plt.ylim(0,hw)
plt.gca().set_aspect('equal')
plt.savefig('sourcedist.png', dpi=1000)
plt.show()
