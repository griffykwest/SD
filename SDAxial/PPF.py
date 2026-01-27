import openmc
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no GUI, file output only
import matplotlib.pyplot as plt
import pandas as pd
from surfaces import *

def pltfix(xyplot):
    n = np.shape(xyplot)[0]

    for i in range(n):
        xyplot[0,i] = 2*xyplot[0,i]
        xyplot[i,0] = 2*xyplot[i,0]
    return xyplot

def qtf(arr):
    x_mirror = np.flip(arr, axis=0)
    right = np.vstack([x_mirror[:-1], (x_mirror[-1] + arr[0]) / 2, arr[1:]])
    left = np.flip(right, axis=1)
    full = np.hstack([left[:, :-1], (left[:, -1:] + right[:, 0:1]) / 2, right[:, 1:]])
    return full

def datatocsv(matrix,filename):
    df = pd.DataFrame(matrix)
    df.to_csv(filename, index=False, header=False)
    return

def get_assy(pin_map, ai, aj, PINS=17):
    """
    Extract an assembly from a pin map. Handles partial assemblies on edges
    """
    n_total = pin_map.shape[0]
    
    # compute start/end indices
    i0 = ai * PINS
    i1 = min(i0 + PINS, n_total)
    j0 = aj * PINS
    j1 = min(j0 + PINS, n_total)
    
    return pin_map[i0:i1, j0:j1]


EV_TO_J = 1.602176634e-19
P_TARGET = 700e6/4 

def intra(batch,z):
    sp = openmc.StatePoint(f'statepoint.{batch}.h5')

    power_tally = sp.get_tally(name='tally 3')
    #hight = z_ta- z_ba

    E_per_source = power_tally.mean[0, 0] 
          # eV / source neutron
    E_per_source_J = E_per_source * EV_TO_J
    

    scale = P_TARGET / E_per_source_J



    tally = sp.get_tally(name = 'tally 1')

    mesh = tally.find_filter(openmc.MeshFilter).mesh

    nx, ny, nz = mesh.dimension

    scores = tally.scores

    heating_idx = scores.index('heating-local')

    mean = tally.mean[:, 0, :]
    volume = np.max(mesh.volumes)
    dx = pitch
    dy = pitch
    height = volume/(dx*dy)
    
    sa = height*np.pi*2*R_co
    cm2m2 = 10000

    heating = mean[:, heating_idx]

    heating_Wm2 = heating * EV_TO_J * scale / sa * cm2m2
    heating_Wm = heating * EV_TO_J * scale / height *100

    heating_3d = heating_Wm.reshape((nx, ny, nz), order='F')

    heating_3d_norm = heating_3d

    heating_min, heating_max = heating_3d_norm.min(), heating_3d_norm.max()
    
    heating_xy = heating_3d[:, :, z].T

    #heating_xy = pltfix(heating_xy)
    #heating_xy = qtf(heating_xy)
    #np.set_printoptions(threshold=np.inf)
    #print(heating_xy)


    return heating_xy


test = intra(4000,20)

def compute_peaking(LHGR_xy, first_size=9, full_size=17, N_assy=7):

    nx, ny = LHGR_xy.shape

    print(nx)

    #multiuplying for proper readings(similar to pltfix)
    weights = np.ones_like(LHGR_xy)
    weights[0, :] *= 2       # first row
    weights[:, 0] *= 2       # first column


    # x and y edges of each assembly
    x_edges = [0] + list(range(first_size, nx+1, full_size))
    y_edges = [0] + list(range(first_size, ny+1, full_size))
    #print(x_edges,y_edges)

    assembly_map = np.zeros_like(LHGR_xy, dtype=int)
    assy_num = 0
    for i in range(len(x_edges)-1):
        for j in range(len(y_edges)-1):
            i0, i1 = x_edges[i], x_edges[i+1]
            j0, j1 = y_edges[j], y_edges[j+1]
            assembly_map[i0:i1, j0:j1] = assy_num
            assy_num += 1
    #print(assembly_map)
    #datatocsv(assembly_map,'assy.csv')
    #datatocsv(LHGR_xy,'heating.csv')

    n_assembly = assy_num


    assembly_sums = np.zeros(n_assembly)
    assembly_counts = np.zeros(n_assembly)

    for a in range(n_assembly):
        mask = assembly_map == a
        assembly_sums[a] = np.sum(LHGR_xy[mask] * weights[mask])
        assembly_counts[a] = np.count_nonzero(mask)

    assembly_avg = assembly_sums / assembly_counts
    FUEL_THRESHOLD = 1e3

    # --------------------------------------------------
    #Fuel identification, making sure that there is true assembly values
    # --------------------------------------------------
    fuel_mask = assembly_avg > FUEL_THRESHOLD

    # --------------------------------------------------
    #Intra-assembly peaking assembly only no ghost values
    # --------------------------------------------------
    Fq_intra = np.full(n_assembly, np.nan)


    for a in range(n_assembly):
        if not fuel_mask[a]:
            continue

        mask = assembly_map == a
        pin_power = LHGR_xy[mask] * weights[mask]

        Fq_intra[a] = pin_power.max() / pin_power.mean()

    # --------------------------------------------------
    # 7) Inter-assembly peaking (fuel only)
    # --------------------------------------------------
    fuel_avgs = assembly_avg[fuel_mask]
    Fq_inter = assembly_avg/ fuel_avgs.mean()
    Fq_inter = np.where(fuel_mask, Fq_inter, np.nan)

    return Fq_intra, Fq_inter, assembly_avg, fuel_mask


Fq_intra, Fq_inter, assembly_avg , fuel_mask = compute_peaking(test, first_size=9, full_size=17, N_assy=7)

np.set_printoptions(linewidth=200)
Fq_intra = Fq_intra.reshape((7,7))
Fq_inter = Fq_inter.reshape((7,7))
print("Inter-assembly PPF:")
print(Fq_inter)

print("Intra-assembly PPFs:")
print(Fq_intra)
#Fq_plot = np.nan_to_num(Fq_intra, nan=0.0)

plt.figure(figsize=(6,6))
plt.imshow(Fq_intra, origin='lower', cmap='inferno', interpolation='nearest')
plt.colorbar(label='Intra-assembly PPF')
plt.title('Quarter-Core Intra-Assembly Peaking Factor')
plt.xlabel('Assembly X Index')
plt.ylabel('Assembly Y Index')
plt.gca().set_aspect('equal')
plt.savefig(f'intrappf.png')

plt.figure(figsize=(6,6))
plt.imshow(Fq_inter, origin='lower', cmap='inferno', interpolation='nearest')
plt.colorbar(label='Intra-assembly PPF')
plt.title('Quarter-Core Inter-Assembly Peaking Factor')
plt.xlabel('Assembly X Index')
plt.ylabel('Assembly Y Index')
plt.gca().set_aspect('equal')
plt.savefig(f'interppf.png')