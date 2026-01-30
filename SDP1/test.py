from pathlib import Path

run_dir = Path("./parametric_runs/smoke_test")
print(run_dir.resolve())      # shows the full absolute path
print(list(run_dir.glob("*"))) 