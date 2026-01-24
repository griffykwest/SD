import openmc
from matax import axial_materials  # your dict of Material objects

# Load the volume calculation
vol_calc = openmc.VolumeCalculation.from_hdf5('volume_1.h5')

# Map material IDs to names
id_to_name = {mat.id: name for name, mat in axial_materials.items()}

# Print volumes with names
print("Material volumes:")
for mat_id, vol in vol_calc.volumes.items():
    name = id_to_name.get(mat_id, f"Unknown (ID {mat_id})")
    print(f"{name} (ID {mat_id}): {vol:.3f} cm^3")

Total_EnergyMWD = 700 * 365 *2  #MWD
UO2_densitygcm3 = 10.15 #g/cm3

uraniumL_material_ids = [mat.id for name, mat in axial_materials.items() if 'UO2L' in name]
uraniumM_material_ids = [mat.id for name, mat in axial_materials.items() if 'UO2M' in name]
uraniumH_material_ids = [mat.id for name, mat in axial_materials.items() if 'UO2H' in name]
moderator_material_ids = [mat.id for name, mat in axial_materials.items() if 'moderator' in name]

# Sum their volumes
total_uraniumL_volumecc = sum(vol_calc.volumes[mat_id] for mat_id in uraniumL_material_ids)
total_uraniumM_volumecc = sum(vol_calc.volumes[mat_id] for mat_id in uraniumM_material_ids)
total_uraniumH_volumecc = sum(vol_calc.volumes[mat_id] for mat_id in uraniumH_material_ids)
total_moderator_volumecc = sum(vol_calc.volumes[mat_id] for mat_id in moderator_material_ids)
total_uranium_volumecc = total_uraniumL_volumecc+total_uraniumM_volumecc+total_uraniumH_volumecc
print(f"Total Luranium volume = {total_uraniumL_volumecc:.3f} cm^3")
print(f"Total Muranium volume = {total_uraniumM_volumecc:.3f} cm^3")
print(f"Total Huranium volume = {total_uraniumH_volumecc:.3f} cm^3")
print(f"Total uranium volume = {total_uranium_volumecc:.3f} cm^3")
print(f"Total moderator volume = {total_moderator_volumecc:.3f} cm^3")

mass_UO2g = total_uranium_volumecc * UO2_densitygcm3
mass_uo2T = mass_UO2g/1000/1000  * 4#g>kg>MT in total core
print(mass_uo2T)
total_burnup = Total_EnergyMWD/ mass_uo2T

print(total_burnup)


