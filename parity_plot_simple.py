import numpy as np
import matplotlib.pyplot as plt
from ase.io import read

# Read DFT and MACE data
dft_data = read("../data/test.extxyz", ":")
mace_data = read("test_mace.extxyz", ":")

e_dft = np.array([a.info["energy"] / len(a) for a in dft_data])
e_mace = np.array([a.info["MACE_energy"] / len(a) for a in mace_data])
f_dft = np.concatenate([a.arrays["forces"].ravel() for a in dft_data])
f_mace = np.concatenate([a.arrays["MACE_forces"].ravel() for a in mace_data])

fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.25))

panels = [
    (axes[0], e_dft, e_mace, "Energy", "eV/atom"),
    (axes[1], f_dft, f_mace, "Force", "eV/Å"),
]

for ax, x, y, name, unit in panels:
    lo = min(x.min(), y.min())
    hi = max(x.max(), y.max())

    # y = x reference line
    ax.plot([lo, hi], [lo, hi], "k--", lw=1)

    # Parity points
    ax.scatter(x, y, s=8, alpha=0.5)

    # RMSE
    rmse = np.sqrt(np.mean((x - y) ** 2)) * 1000

    ax.set(
        xlabel=f"DFT {name} ({unit})",
        ylabel=f"MACE {name} ({unit})",
        xlim=(lo, hi),
        ylim=(lo, hi),
        aspect="equal",
        title=f"{name} RMSE = {rmse:.1f} m{unit}",
    )

plt.tight_layout()
plt.savefig("parity.png", dpi=200, bbox_inches="tight")
plt.show()
