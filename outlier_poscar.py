from ase.io import read, write
import numpy as np, pandas as pd, os

REF  = "../data/train.extxyz"
PRED = "train_pred.extxyz"
OUTDIR = "train_outlier_poscars"

ref  = read(REF, ":")
pred = read(PRED, ":")
assert len(ref) == len(pred), f"frame count mismatch: {len(ref)} vs {len(pred)}"

# --- confirm key names before trusting anything ---
print("pred info keys:", list(pred[0].info.keys()))
print("pred array keys:", list(pred[0].arrays.keys()))

E_KEY = "MACE_energy"      # adjust if the print above says otherwise
F_KEY = "MACE_forces"

rows = []
for i, (a, b) in enumerate(zip(ref, pred)):
    n = len(a)
    if n > 1:
        d = a.get_all_distances(mic=bool(a.pbc.any()))
        min_dist = d[np.triu_indices(n, 1)].min()
    else:
        min_dist = np.nan
    rows.append(dict(
        idx=i, natoms=n,
        formula=a.get_chemical_formula(),
        config_type=a.info.get("config_type", "NA"),
        e_ref=a.get_potential_energy() / n,
        e_pred=b.info[E_KEY] / n,
        dE=b.info[E_KEY] / n - a.get_potential_energy() / n,
        max_f_err=np.abs(b.arrays[F_KEY] - a.get_forces()).max(),
        volume=a.get_volume() / n if a.pbc.any() else np.nan,
        min_dist=min_dist,
    ))

df = pd.DataFrame(rows)
df.to_csv("all_frames.csv", index=False)          # keep the full set too

bad = df[df.dE > 0.05].sort_values("dE", ascending=False)
print(bad.to_string())
bad.to_csv("train_overpred.csv", index=False)

# --- one POSCAR per frame ---
os.makedirs(OUTDIR, exist_ok=True)
for _, r in bad.iterrows():
    i = int(r.idx)
    atoms = ref[i]
    fname = f"{OUTDIR}/frame{i:05d}_dE{r.dE:+.3f}_{r.formula}.vasp"
    write(fname, atoms, format="vasp",
          direct=True, sort=True, vasp5=True)
print(f"wrote {len(bad)} POSCARs to {OUTDIR}/")

ref = read("../data/train.extxyz", ":")
bad_idx = set(pd.read_csv("train_overpred.csv").idx.astype(int))

keep   = [a for i, a in enumerate(ref) if i not in bad_idx]
remove = [a for i, a in enumerate(ref) if i in bad_idx]

write("train_clean.extxyz", keep)
write("train_removed.extxyz", remove)      # never just delete
print(f"{len(ref)} -> kept {len(keep)}, removed {len(remove)}")
