from pymatgen.io.vasp import Oszicar


# get the kinetic energy
oszicar = Oszicar("../tests/data/oszicar/oszicar")

# get the kinetic energy
print(oszicar.ionic_steps[-1])
