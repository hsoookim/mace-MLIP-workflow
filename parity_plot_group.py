import numpy as np
import matplotlib.pyplot as plt
from ase.io import read

# ----------------------------------------------------------------------
# Define structure groups based on the source_file path stored in extxyz
# ----------------------------------------------------------------------
GROUPS = {
    "K2CO3": "/home/hk26346/Project1_TES/K2CO3/",
    "K2CO3_15H2O": "/home/hk26346/Project1_TES/K2CO3_15H2O/",
}
def get_group(atoms):
    """Return the group name based on the stored source_file path."""
    source_path = atoms.info["source_file"]

    for group_name, path_prefix in GROUPS.items():
        if source_path.startswith(path_prefix):
            return group_name

    return "other"

# ----------------------------------------------------------------------
# Read DFT reference data and MACE predictions
# ----------------------------------------------------------------------
dft_data = read("../data/test.extxyz", index=":")
mace_data = read("test_mace.extxyz", index=":")

group_labels = [get_group(atoms) for atoms in dft_data]

energy_dft = np.array([atoms.info["energy"] / len(atoms) for atoms in dft_data])
energy_mace = np.array([atoms.info["MACE_energy"] / len(atoms) for atoms in mace_data])
energy_groups = np.array(group_labels)
force_dft = np.concatenate([atoms.arrays["forces"].ravel() for atoms in dft_data])
force_mace = np.concatenate([atoms.arrays["MACE_forces"].ravel() for atoms in mace_data])
force_groups = np.concatenate([np.repeat(group, 3 * len(atoms))for atoms, group in zip(dft_data, group_labels)])

# ----------------------------------------------------------------------
# Color settings
# ----------------------------------------------------------------------
groups = sorted(set(group_labels))
colors = {
    group: f"C{i}"
    for i, group in enumerate(groups)
}

fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.25))

panels = [
    (axes[0], energy_dft, energy_mace, energy_groups,"Energy","eV/atom"),
    (axes[1], force_dft, force_mace, force_groups, "Force", "eV/Å")
]


# ----------------------------------------------------------------------
# Create parity plots
# ----------------------------------------------------------------------
for ax, x, y, group_array, label, unit in panels:

    # Use the same axis range for DFT and MACE
    lower = min(x.min(), y.min())
    upper = max(x.max(), y.max())

    # Ideal y = x reference line
    ax.plot([lower, upper],[lower, upper],"k--",linewidth=1, zorder=0)

    # Plot each structure group separately
    for group in groups:
        mask = group_array == group

        ax.scatter(x[mask],y[mask],s=8,alpha=0.5,color=colors[group],label=group)

    # Overall RMSE
    rmse = np.sqrt(np.mean((x - y) ** 2)) * 1000

    ax.set_xlabel(f"DFT {label} ({unit})")
    ax.set_ylabel(f"MACE {label} ({unit})")
    ax.set_xlim(lower, upper)
    ax.set_ylim(lower, upper)
    ax.set_aspect("equal")
    ax.set_title(f"{label} RMSE = {rmse:.1f} m{unit}")

axes[1].legend(fontsize=8)

plt.tight_layout()
plt.savefig("parity_by_group.png", dpi=200, bbox_inches="tight")
plt.show()
