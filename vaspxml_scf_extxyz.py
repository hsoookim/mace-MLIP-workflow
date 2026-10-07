import glob
from ase.io import read, write
from pathlib import Path

all_atoms = []
dirs = ["soft"]

for d in dirs:
    files = sorted(glob.glob(f"./*/{d}/vasprun_*"))

    for path in files:
        print(f"Reading {path}")
        atoms = read(path, index=-1, format="vasp-xml") #last ionic step
        atoms.info["source_file"] = str(Path(path).resolve())
        all_atoms.append(atoms)

print(f"\nTotal structures collected: {len(all_atoms)}")
write(f"train_set_{len(all_atoms)}.extxyz", all_atoms)
