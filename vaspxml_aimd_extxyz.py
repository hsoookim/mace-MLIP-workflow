import glob
from ase.io import read, write
from pathlib import Path

STEP = 1000  # keep every 1000th step

all_atoms = []
dirs = ["001", "002", "003", "004", "005"]

for d in dirs:
    files = sorted(glob.glob(f"./{d}/*/vasprun_*"))

    for path in files:
        print(f"Reading {path}")
        frames = read(path, index=":", format="vasp-xml")  # all ionic steps

        n = len(frames)

        if n == 0:
            print("  No frames found, skipping")
            continue

        # Keep 0th, every STEP-th frame, and the last frame
        # set() prevents duplicate indices
        indices = sorted(set(range(0, n, STEP)) | {n - 1})

        for i in indices:
            atoms = frames[i]
            atoms.info["source_file"] = str(Path(path).resolve())
            atoms.info["frame_index"] = i
            all_atoms.append(atoms)

        print(f"  {n} frames found, kept {len(indices)}")

print(f"\nTotal structures collected: {len(all_atoms)}")
write(f"Train_Set_AIMD_{len(all_atoms)}.extxyz", all_atoms)
