from setup import ReactorModel

"""
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
"""

model = ReactorModel()

results = model.run_single_case(
    run_name="smoke_test",
    params={'ppb': 1000,'boron_ppm':0},
    cleanup=True
)

print(results)