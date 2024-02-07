from pymatgen.io.vasp import Vasprun, Outcar, Oszicar

vasprun = Vasprun("../tests/data/vasprun/vasprun.xml")

# get the total energy
energy = vasprun.final_energy
print(energy)

# get all energies
for i in range(len(vasprun.ionic_steps)):
    print(vasprun.ionic_steps[i]['electronic_steps'][-1]['e_wo_entrp'])

# get the kinetic energy
oszicar = Oszicar("../tests/data/oszicar/oszicar")

# get the kinetic energy
print(oszicar.ionic_steps[-1])




