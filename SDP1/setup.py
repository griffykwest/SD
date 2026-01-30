import openmc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from typing import Dict, List, Tuple, Optional
import shutil
import os

# Import your existing modules
"""from matax import *
from lattices import lattices, universes, cells
from surfaces import *
from specialinputs import axial_control_rod_fixed
from densitylookup import *"""
from All import lattices, universes, cells, axial_materials
from surfaces import *
from specialinputs import axial_control_rod_fixed
from densitylookup import *

class ReactorModel:
    """
    Wrapper class for the reactor model that allows parameter variation
    """
    
    def __init__(self, base_dir: str = "./parametric_runs"):
        """
        Initialize the reactor model
        
        Parameters:
        -----------
        base_dir : str
            Base directory for storing parametric study results
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Store default parameters
        self.default_params = {
            'boron_ppm': 2200,
            'batches': 2000,
            'ppb': 10000,
            'inactive': 200,
            'A_bank': 0.0,
            'B_bank': 0.0,
            'C_bank': 0.0,
            'shutdown_bank': 0.0,
            'T_mod_inlet': 290 + 273.15,
            'T_mod_outlet': 310 + 273.15,
            'T_fuel_avg': 700,
            'T_fuel_amp': 0
        }
        
    def setup_geometry(self, A_bank=0.0, B_bank=0.0, C_bank=0.0, shutdown_bank=0.0):
        """
        Set up the reactor geometry with specified control rod positions
        
        Parameters:
        -----------
        A_bank, B_bank, C_bank, shutdown_bank : float
            Control rod insertion fraction (0 = fully out, 1 = fully in)
        """
        # Import needs to be fresh for each geometry
        from newuniverses import universes, cells
        from lattices import lattices
        
        # Set up core lattice

        
        # Set up root universe
        geometry = openmc.Geometry()
        geometry.root_universe = universes['Root']
        
        return geometry
    
    def setup_settings(self, batches=2000, ppb=10000, inactive=200, 
                      T_mod_inlet=290+273.15, T_mod_outlet=310+273.15):
        """
        Set up OpenMC settings
        """
        settings = openmc.Settings()
        settings.batches = batches
        settings.inactive = inactive
        settings.particles = ppb
        settings.temperature = {
            'method': 'interpolation',
            'range': (293.0, 1800.0),
            'tolerance': 100.0
        }
        
        # Source definition
        source = openmc.IndependentSource()
        r_dist = openmc.stats.Uniform(a=0.0, b=r_core)
        phi_dist = openmc.stats.Uniform(a=0.0, b=(1/2)*np.pi)
        z_dist = openmc.stats.Uniform(a=z_ba, b=z_ta)
        
        source.space = openmc.stats.CylindricalIndependent(
            r=r_dist, phi=phi_dist, z=z_dist, origin=(0.0, 0.0, 0.0)
        )
        source.only_fissionable = True
        settings.source = source
        
        return settings
    
    def run_single_case(self, run_name: str, params: Dict, 
                       cleanup: bool = True) -> Dict:
        """
        Run a single OpenMC case with specified parameters
        
        Parameters:
        -----------
        run_name : str
            Name for this run (used for directory)
        params : dict
            Dictionary of parameters to vary
        cleanup : bool
            Whether to clean up XML files after run
            
        Returns:
        --------
        results : dict
            Dictionary containing keff, uncertainty, and other results
        """
        run_dir = self.base_dir / run_name
        run_dir.mkdir(exist_ok=True)
        
        # Change to run directory
        original_dir = os.getcwd()
        os.chdir(run_dir)
        
        try:
            # Update materials with new parameters
            if 'boron_ppm' in params:
                # Need to regenerate materials with new boron
                self._regenerate_materials(params)
            
            if 'T_mod_inlet' in params or 'T_mod_outlet' in params:
                self._regenerate_materials(params)
                
            if 'T_fuel_avg' in params or 'T_fuel_amp' in params:
                self._regenerate_materials(params)

            # Set up materials  ← ADD THIS
            from All import axial_materials

            materials = openmc.Materials(axial_materials.values())
            materials.export_to_xml()
            
            # Set up geometry with control rod positions
            geometry = self.setup_geometry(
                A_bank=params.get('A_bank', 0.0),
                B_bank=params.get('B_bank', 0.0),
                C_bank=params.get('C_bank', 0.0),
                shutdown_bank=params.get('shutdown_bank', 0.0)
            )
            geometry.export_to_xml()
            
            # Set up settings
            settings = self.setup_settings(
                batches=params.get('batches', 2000),
                ppb=params.get('ppb', 10000),
                inactive=params.get('inactive', 200),
                T_mod_inlet=params.get('T_mod_inlet', 290+273.15),
                T_mod_outlet=params.get('T_mod_outlet', 310+273.15)
            )
            settings.export_to_xml()
            
            # Set up tallies
            from tally import tallies
            tallies_file = openmc.Tallies(tallies.values())
            tallies_file.export_to_xml()
            
            # Run OpenMC
            openmc.run()
            
            # Extract results
            sp = openmc.StatePoint(f'statepoint.{params.get("batches", 2000)}.h5')
            keff = sp.keff
            
            results = {
                'keff': keff.n,
                'keff_uncertainty': keff.s,
                'params': params,
                'run_dir': str(run_dir)
            }
            
            # Save results
            with open('results.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            return results
            
        finally:
            os.chdir(original_dir)
            
            if cleanup:
                # Clean up XML files but keep results
                for xml_file in run_dir.glob('*.xml'):
                    xml_file.unlink()
    
    def _regenerate_materials(self, params: Dict):
        """
        Regenerate materials with new parameters
        This is a placeholder - you'll need to implement based on your matax.py structure
        """
        # This would need to call the material generation functions from matax.py
        # with the new parameters
        pass


    