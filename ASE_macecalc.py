import torch

_orig_jit_load = torch.jit.load
def _cpu_jit_load(*args, **kwargs):
    kwargs["map_location"] = torch.device("cpu")
    return _orig_jit_load(*args, **kwargs)
torch.jit.load = _cpu_jit_load

from mace.calculators import MACECalculator
from ase.io import read
from ase.md.nose_hoover_chain import NoseHooverChainNVT
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary, ZeroRotation
from ase.md import MDLogger
from ase.io.trajectory import Trajectory
from ase import units

atoms = read('structure.data', format='lammps-data', Z_of_type={1: 6, 2: 1, 3: 19, 4: 8})
calc = MACECalculator(
    model_paths='/path/to/your/mace.model',
    device='cpu',
    default_dtype='float64',
)
atoms.calc = calc

# initial velocities
MaxwellBoltzmannDistribution(atoms, temperature_K=300, force_temp=True, rng=None)
Stationary(atoms)
ZeroRotation(atoms)

dyn = NoseHooverChainNVT(
    atoms,
    timestep=0.5 * units.fs,
    temperature_K=300,
    tdamp=50 * units.fs,
    tchain=3,      # LAMMPS default tchain
    tloop=1,
)

# thermo 1000 / dump 1000
dyn.attach(MDLogger(dyn, atoms, 'md.log', header=True, stress=False), interval=10)
dyn.attach(Trajectory('traj.traj', 'w', atoms).write, interval=10)

dyn.run(2000)
