import openmc
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no GUI, file output only
import matplotlib.pyplot as plt
import pandas as pd
from surfaces import *


## doubles the edges to make them correct
def pltfix(xyplot):
    n = np.shape(xyplot)[0]

    for i in range(n):
        xyplot[0,i] = 2*xyplot[0,i]
        xyplot[i,0] = 2*xyplot[i,0]
    return xyplot


#was to help bill make the qtf function now just here
def datatocsv(matrix,filename):
    df = pd.DataFrame(matrix)
    df.to_csv(filename, index=False, header=False)
    return


## for making quater core go to full core
def qtf(arr):
    x_mirror = np.flip(arr, axis=0)
    right = np.vstack([x_mirror[:-1], (x_mirror[-1] + arr[0]) / 2, arr[1:]])
    left = np.flip(right, axis=1)
    full = np.hstack([left[:, :-1], (left[:, -1:] + right[:, 0:1]) / 2, right[:, 1:]])
    return full



EV_TO_J = 1.602176634e-19
P_TARGET = 700e6/4  # 700 MWth
# plotting function for xy slices
# 15 is the middle slice and the core goes from 5-25
def xyslice(batch , z):
    
    sp = openmc.StatePoint(f'statepoint.{batch}.h5')

    power_tally = sp.get_tally(name='tally 3')
    E_per_source = power_tally.mean[0, 0] 
          # eV / source neutron
    E_per_source_J = E_per_source * EV_TO_J
    

    scale = P_TARGET / E_per_source_J
    



    tally = sp.get_tally(name = 'tally 1')

    mesh = tally.find_filter(openmc.MeshFilter).mesh

    nx, ny, nz = mesh.dimension

    scores = tally.scores

    flux_idx = scores.index('flux')
    fission_idx = scores.index('fission')
    heating_idx = scores.index('heating-local')

    mean = tally.mean[:, 0, :]
    volume = np.max(mesh.volumes)
    dx = pitch
    dy = pitch
    hight = volume/(dx*dy)
    
    sa = hight*np.pi*2*R_co
    cm2m2 = 10000

    flux = mean[:, flux_idx]

    fission = mean[:, fission_idx] 

    heating = mean[:, heating_idx]
    volume = np.max(mesh.volumes)
    volumes = mesh.volumes.reshape((nx, ny, nz))[:, :, z]

    ## for q'' put the 2 for heating 3d
    heating_Wm2 = heating * EV_TO_J * scale / sa * cm2m2
    heating_Wm = heating * EV_TO_J * scale / hight *100
   

    flux_3d = flux.reshape((nx, ny, nz), order='F')

    fission_3d = fission.reshape((nx, ny, nz), order='F')

    heating_3d = heating_Wm.reshape((nx, ny, nz), order='F')




    flux_3d_norm = flux_3d #/ mesh.volumes.reshape((nx, ny, nz), order='F')
    fission_3d_norm = fission_3d #/ mesh.volumes.reshape((nx, ny, nz), order='F')

    # get min and max for the whole volume
    flux_min, flux_max = flux_3d_norm.min(), flux_3d_norm.max()
    fission_min, fission_max = fission_3d_norm.min(), fission_3d_norm.max()


    flux_xy = flux_3d[:,:,z]
    flux_xy = flux_xy #/ volumes
    flux_xy = flux_xy.T

    flux_xy = pltfix(flux_xy)


    ## acounting for the half sized points


    fission_xy = fission_3d[:,:,z]
    fission_xy = fission_xy #/ volumes
    fission_xy = fission_xy.T

    fission_xy = pltfix(fission_xy)

    heating_xy = heating_3d[:, :, z].T

    heating_xy = pltfix(heating_xy)


    #fluxfile = "fluxfile.csv"
    #fissionfile = "fissionfile.csv"
    #heatingfile = "heatingfile.csv"

    #datatocsv(flux_xy,fluxfile)
    #datatocsv(fission_xy,fissionfile)
    #datatocsv(heating_xy,heatingfile)

    flux_xy = qtf(flux_xy)
    fission_xy = qtf(fission_xy)
    heating_xy = qtf(heating_xy)


    x_edges = np.linspace(-mesh.upper_right[0], mesh.upper_right[0], nx*2-1)
    y_edges = np.linspace(-mesh.upper_right[1], mesh.upper_right[1], ny*2-1)

    plt.figure(figsize=(8, 6), dpi=1000)
    plt.pcolormesh(x_edges, y_edges, flux_xy, shading='auto', cmap='bwr', vmin=flux_min, vmax=flux_max)
    plt.colorbar(label='Flux [#/cm²/s]')
    plt.xlabel('X [cm]')
    plt.ylabel('Y [cm]')
    plt.gca().set_aspect('equal')
    plt.savefig(f'{batch}flux_xy_{z}.png')

    plt.figure(figsize=(8, 6), dpi=1000)
    plt.pcolormesh(x_edges, y_edges, fission_xy, shading='auto', cmap='bwr', vmin=fission_min, vmax=fission_max)
    plt.colorbar(label='Fission [#/s]')
    plt.xlabel('X [cm]')
    plt.ylabel('Y [cm]')
    plt.gca().set_aspect('equal')
    #plt.savefig(f'{batch}fission_xy_{z}.png')

    plt.figure(figsize=(8, 6), dpi=1000)
    plt.pcolormesh(
        x_edges, y_edges,
        heating_xy,      # MW per mesh cell
        shading='auto',
        cmap='bwr'
    )
    plt.colorbar(label='Heating [W/m]')
    plt.xlabel('X [cm]')
    plt.ylabel('Y [cm]')
    plt.gca().set_aspect('equal')
    plt.savefig(f'{batch}heating_xy_{z}.png')
    return
"""xyslice(2000, 6)
xyslice(2000, 10)
xyslice(2000, 15)
"""

# plotting function for an xz slice 111 is the middle
def xzslice(batch, y):
    sp = openmc.StatePoint(f'statepoint.{batch}.h5')

    power_tally = sp.get_tally(name='tally 3')
    E_per_source = power_tally.mean[0, 0]        # eV / source neutron
    E_per_source_J = E_per_source * EV_TO_J

    scale = P_TARGET / E_per_source_J  

    tally = sp.get_tally(name = 'tally 1')

    mesh = tally.find_filter(openmc.MeshFilter).mesh

    nx, ny, nz = mesh.dimension

    scores = tally.scores

    flux_idx = scores.index('flux')
    fission_idx = scores.index('fission')
    heating_idx = scores.index('heating-local')

    mean = tally.mean[:, 0, :]
    volume = np.max(mesh.volumes)
    flux = mean[:, flux_idx]

    fission = mean[:, fission_idx] 
    heating = mean[:, heating_idx]
    volume = np.max(mesh.volumes)
    volumes = mesh.volumes.reshape((nx, ny, nz))[:, y, :]
    heating_W = heating * EV_TO_J * scale*1000 / volume

    flux_3d = flux.reshape((nx, ny, nz), order='F')

    fission_3d = fission.reshape((nx, ny, nz), order='F')

    heating_3d = heating_W.reshape((nx, ny, nz), order='F')


    flux_3d_norm = flux_3d #/ mesh.volumes.reshape((nx, ny, nz), order='F')
    fission_3d_norm = fission_3d #/ mesh.volumes.reshape((nx, ny, nz), order='F')

    # get min and max for the whole volume
    flux_min, flux_max = flux_3d_norm.min(), flux_3d_norm.max()
    fission_min, fission_max = fission_3d_norm.min(), fission_3d_norm.max()

    flux_xz = flux_3d[:,y,:]
    flux_xz = flux_xz #/ volumes
    flux_xz = flux_xz.T

    fission_xz = fission_3d[:,y,:]
    fission_xz = fission_xz #/ volumes
    fission_xz = fission_xz.T

    heating_xz = heating_3d[:, y, :].T

    # Mesh edges along X and Z
    x_edges = np.linspace(mesh.lower_left[0], mesh.upper_right[0], nx+1)
    z_edges = np.linspace(mesh.lower_left[2], mesh.upper_right[2], nz+1)


    plt.figure(dpi=150)
    plt.pcolormesh(x_edges, z_edges, flux_xz, shading='auto', cmap='bwr', vmin=flux_min, vmax=flux_max)
    plt.colorbar(label='Flux [#/cm²/s]')
    plt.xlabel('X [cm]')
    plt.ylabel('Z [cm]')
    plt.gca().set_aspect('equal')
    plt.savefig(f'{batch}flux_xz_{y}.png')

    plt.figure(dpi=150)
    plt.pcolormesh(x_edges, z_edges, fission_xz, shading='auto', cmap='bwr', vmin=fission_min, vmax=fission_max)
    plt.colorbar(label='Fission [#/s]')
    plt.xlabel('X [cm]')
    plt.ylabel('Z [cm]')
    plt.gca().set_aspect('equal')
    #plt.savefig(f'{batch}fission_xz_{y}.png')

    plt.figure(dpi=150)
    plt.pcolormesh(
        x_edges, z_edges,
        heating_xz / 1e6,      # MW per mesh cell
        shading='auto',
        cmap='bwr'
    )
    plt.colorbar(label='Heating [kW per cm$^3$]')
    plt.xlabel('X [cm]')
    plt.ylabel('Y [cm]')
    plt.gca().set_aspect('equal')
    plt.savefig(f'{batch}heating_xz_{y}.png')
    return

"""xzslice(2000, 110)
xzslice(2000, 65)
xzslice(2000, 111)
"""



