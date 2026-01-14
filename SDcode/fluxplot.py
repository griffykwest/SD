import openmc
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no GUI, file output only
import matplotlib.pyplot as plt
import pandas as pd

# plotting function for xy slices
# 15 is the middle slice and the core goes from 5-25
def xyslice(batch , z):
    
    sp = openmc.StatePoint(f'statepoint.{batch}.h5')

    tally = sp.get_tally(name = 'tally 1')

    mesh = tally.find_filter(openmc.MeshFilter).mesh

    nx, ny, nz = mesh.dimension

    scores = tally.scores

    flux_idx = scores.index('flux')
    fission_idx = scores.index('fission')

    mean = tally.mean[:, 0, :]
    volume = np.max(mesh.volumes)
    flux = mean[:, flux_idx]

    fission = mean[:, fission_idx] 

    flux_3d = flux.reshape((nx, ny, nz), order='F')

    fission_3d = fission.reshape((nx, ny, nz), order='F')

    volume = np.max(mesh.volumes)
    volumes = mesh.volumes.reshape((nx, ny, nz))[:, :, z]

    flux_3d_norm = flux_3d #/ mesh.volumes.reshape((nx, ny, nz), order='F')
    fission_3d_norm = fission_3d #/ mesh.volumes.reshape((nx, ny, nz), order='F')

    # get min and max for the whole volume
    flux_min, flux_max = flux_3d_norm.min(), flux_3d_norm.max()
    fission_min, fission_max = fission_3d_norm.min(), fission_3d_norm.max()


    flux_xy = flux_3d[:,:,z]
    flux_xy = flux_xy #/ volumes
    flux_xy = flux_xy.T

    fission_xy = fission_3d[:,:,z]
    fission_xy = fission_xy #/ volumes
    fission_xy = fission_xy.T

    x_edges = np.linspace(mesh.lower_left[0], mesh.upper_right[0], nx+1)
    y_edges = np.linspace(mesh.lower_left[1], mesh.upper_right[1], ny+1)

    plt.figure(dpi=150)
    plt.pcolormesh(x_edges, y_edges, flux_xy, shading='auto', cmap='bwr', vmin=flux_min, vmax=flux_max)
    plt.colorbar(label='Flux [#/cm²/s]')
    plt.xlabel('X [cm]')
    plt.ylabel('Y [cm]')
    plt.gca().set_aspect('equal')
    plt.savefig(f'{batch}flux_xy_{z}.png')

    plt.figure(dpi=150)
    plt.pcolormesh(x_edges, y_edges, fission_xy, shading='auto', cmap='bwr', vmin=fission_min, vmax=fission_max)
    plt.colorbar(label='Fission [#/s]')
    plt.xlabel('X [cm]')
    plt.ylabel('Y [cm]')
    plt.gca().set_aspect('equal')
    plt.savefig(f'{batch}fission_xy_{z}.png')
    return

"""xyslice(2000, 6)
xyslice(2000, 10)
xyslice(2000, 15)
"""
# plotting function for an xz slice 111 is the middle
def xzslice(batch, y):
    sp = openmc.StatePoint(f'statepoint.{batch}.h5')

    tally = sp.get_tally(name = 'tally 1')

    mesh = tally.find_filter(openmc.MeshFilter).mesh

    nx, ny, nz = mesh.dimension

    scores = tally.scores

    flux_idx = scores.index('flux')
    fission_idx = scores.index('fission')

    mean = tally.mean[:, 0, :]
    volume = np.max(mesh.volumes)
    flux = mean[:, flux_idx]

    fission = mean[:, fission_idx] 

    flux_3d = flux.reshape((nx, ny, nz), order='F')

    fission_3d = fission.reshape((nx, ny, nz), order='F')

    volume = np.max(mesh.volumes)
    volumes = mesh.volumes.reshape((nx, ny, nz))[:, y, :]

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
    plt.savefig(f'{batch}fission_xz_{y}.png')
    return

"""xzslice(2000, 110)
xzslice(2000, 65)
xzslice(2000, 111)
"""
