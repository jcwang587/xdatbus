import os
import shutil
from ase import Atom
from xdatbus_utils import unwrap
from ase.io import read, write
from pymatgen.io.vasp.outputs import Xdatcar

# Define the path to the XDATCAR file
AIMD_PATH = "B:/projects/86_Metad_LLTO_pbc/"
N0_OV0_PATH = "pbc_test_1"
file_list = os.listdir(AIMD_PATH + N0_OV0_PATH)
run_list = [run for run in file_list if 'RUN' in run]
xdatcar_U1_N0_OV0_2000K = [AIMD_PATH + N0_OV0_PATH + "/RUN" + str(i + 1) + "/XDATCAR" for i in range(len(run_list))]
xdatcar_U1_N0_OV0_2000K_latest = AIMD_PATH + N0_OV0_PATH + "/XDATCAR"

local_xdatcar_files_raw = "./xdatcar_files_raw"
local_xdatcar_files_wrap = "./xdatcar_files_wrap"

# Clear the directory
if os.path.exists(local_xdatcar_files_raw):
    shutil.rmtree(local_xdatcar_files_raw)
os.mkdir(local_xdatcar_files_raw)
if os.path.exists(local_xdatcar_files_wrap):
    shutil.rmtree(local_xdatcar_files_wrap)
os.mkdir(local_xdatcar_files_wrap)

# Copy the XDATCAR file to the current directory
print("Copying XDATCAR files to the current directory ...")
i = 0
for i in range(len(xdatcar_U1_N0_OV0_2000K)):
    shutil.copy(xdatcar_U1_N0_OV0_2000K[i], "./xdatcar_files_raw/XDATCAR_" + str(i + 1))
shutil.copy(xdatcar_U1_N0_OV0_2000K_latest, "./xdatcar_files_raw/XDATCAR_" + str(i + 2))

# Extract the O, Ti and La coordinates from the first image of the XDATCAR file
atoms = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].atomic_numbers
Li_index = [i for i, x in enumerate(atoms) if x == 3]
O_index = [i for i, x in enumerate(atoms) if x == 8]
Ti_index = [i for i, x in enumerate(atoms) if x == 22]
La_index = [i for i, x in enumerate(atoms) if x == 57]
Li_coord = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].cart_coords[Li_index]
O_coord = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].cart_coords[O_index]
Ti_coord = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].cart_coords[Ti_index]
La_coord = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].cart_coords[La_index]

# Extract the lattice vectors from the first image of the XDATCAR file
a = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].lattice.a
b = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].lattice.b
c = Xdatcar("./xdatcar_files_raw/XDATCAR_1").structures[0].lattice.c

# Get the number of AIMD runs
mdrun = len(xdatcar_U1_N0_OV0_2000K) + 1

# Wrap Li and fix O, Ti and La in the raw XDATCAR files using ASE
for i in range(mdrun):
    xdatcar = read("./xdatcar_files_raw/XDATCAR_" + str(i + 1), format='vasp-xdatcar', index=':')
    # Fix the O, Ti and La atoms
    for s in range(len(xdatcar)):
        for oi in range(len(O_coord)):
            xdatcar[s].positions[O_index[oi]] = O_coord[oi]
        for tii in range(len(Ti_coord)):
            xdatcar[s].positions[Ti_index[tii]] = Ti_coord[tii]
        for lai in range(len(La_coord)):
            xdatcar[s].positions[La_index[lai]] = La_coord[lai]
    # Write the new wrapped XDATCAR file
    write("./xdatcar_files_wrap/XDATCAR_" + str(i + 1), format='vasp-xdatcar', images=xdatcar)
    print("XDATCAR_" + str(i + 1) + " is wrapped, fixed and duplicated.")

# Combine the wrapped XDATCAR files into one XDATCAR file (XDATBUS) using pymatgen
print("Combining XDATCAR files into one XDATCAR file ...")
xdatbus = Xdatcar("./xdatcar_files_wrap/XDATCAR_1")

for i in range(mdrun - 1):
    xdatbus.concatenate("./xdatcar_files_wrap/XDATCAR_" + str(i + 2))
    print("XDATCAR_" + str(i + 2) + " is concatenated.")
xdatbus.write_file('XDATBUS')

# Convert the XDATCAR file to xyz format
print("Converting XDATCAR to xyz format ...")
xdatbusxyz = read('XDATBUS', format='vasp-xdatcar', index=':')
write('XDATBUS.xyz', xdatbusxyz, format='xyz')

# Unwrap the Li atoms in the xyz file
unwrap("XDATBUS", "XDATBUS.xyz")

# Duplicate the xyz file
print("Duplicating the xyz file ...")
xyz = read("XDATBUS_unwrapped.xyz", index=':')

# Extract the O, Ti and La coordinates from the first image of the XDATCAR file
xyz_atoms = xyz[0].get_atomic_numbers()
O_xyz_index = [i for i, x in enumerate(xyz_atoms) if x == 8]
Ti_xyz_index = [i for i, x in enumerate(xyz_atoms) if x == 22]
La_xyz_index = [i for i, x in enumerate(xyz_atoms) if x == 57]
O_xyz_coord = xyz[0].positions[O_index]
Ti_xyz_coord = xyz[0].positions[Ti_index]
La_xyz_coord = xyz[0].positions[La_index]

for s in range(len(xyz)):
    for oi in range(len(O_xyz_coord)):
        xyz[s].append(Atom(symbol='O', position=O_xyz_coord[oi] + [a, 0, 0]))
        xyz[s].append(Atom(symbol='O', position=O_xyz_coord[oi] + [-a, 0, 0]))
        xyz[s].append(Atom(symbol='O', position=O_xyz_coord[oi] + [0, 0, c]))
        xyz[s].append(Atom(symbol='O', position=O_xyz_coord[oi] + [0, 0, -c]))
        xyz[s].append(Atom(symbol='O', position=O_xyz_coord[oi] + [a, 0, c]))
        xyz[s].append(Atom(symbol='O', position=O_xyz_coord[oi] + [a, 0, -c]))
        xyz[s].append(Atom(symbol='O', position=O_xyz_coord[oi] + [-a, 0, c]))
        xyz[s].append(Atom(symbol='O', position=O_xyz_coord[oi] + [-a, 0, -c]))
    for tii in range(len(Ti_xyz_coord)):
        xyz[s].append(Atom(symbol='Ti', position=Ti_xyz_coord[tii] + [a, 0, 0]))
        xyz[s].append(Atom(symbol='Ti', position=Ti_xyz_coord[tii] + [-a, 0, 0]))
        xyz[s].append(Atom(symbol='Ti', position=Ti_xyz_coord[tii] + [0, 0, c]))
        xyz[s].append(Atom(symbol='Ti', position=Ti_xyz_coord[tii] + [0, 0, -c]))
        xyz[s].append(Atom(symbol='Ti', position=Ti_xyz_coord[tii] + [a, 0, c]))
        xyz[s].append(Atom(symbol='Ti', position=Ti_xyz_coord[tii] + [a, 0, -c]))
        xyz[s].append(Atom(symbol='Ti', position=Ti_xyz_coord[tii] + [-a, 0, c]))
        xyz[s].append(Atom(symbol='Ti', position=Ti_xyz_coord[tii] + [-a, 0, -c]))
    for lai in range(len(La_xyz_coord)):
        xyz[s].append(Atom(symbol='La', position=La_xyz_coord[lai] + [a, 0, 0]))
        xyz[s].append(Atom(symbol='La', position=La_xyz_coord[lai] + [-a, 0, 0]))
        xyz[s].append(Atom(symbol='La', position=La_xyz_coord[lai] + [0, 0, c]))
        xyz[s].append(Atom(symbol='La', position=La_xyz_coord[lai] + [0, 0, -c]))
        xyz[s].append(Atom(symbol='La', position=La_xyz_coord[lai] + [a, 0, c]))
        xyz[s].append(Atom(symbol='La', position=La_xyz_coord[lai] + [a, 0, -c]))
        xyz[s].append(Atom(symbol='La', position=La_xyz_coord[lai] + [-a, 0, c]))
        xyz[s].append(Atom(symbol='La', position=La_xyz_coord[lai] + [-a, 0, -c]))
    print("Image " + str(s + 1) + " is duplicated.")
for s in range(len(xyz)):
    xyz[s].cell = None
    xyz[s].pbc = False
write("./XDATRAIN.xyz", format='xyz', images=xyz)
