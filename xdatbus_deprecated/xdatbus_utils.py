import numpy as np
from copy import deepcopy
from ase.io import read


def read_lat_vec(xdatcar_dir):
    """Read the lattice vectors from the first image of the XDATCAR file."""
    xdatcar = read(xdatcar_dir, format='vasp-xdatcar')
    lat_vec = np.array(xdatcar.get_cell())
    return lat_vec


def unwrap(xdatacar_path, xyz_path):
    # You can read the lattice vectors from lattice.vector file
    L = read_lat_vec(xdatacar_path)

    # Run the MSD calculator with XDATCAR_frac.xyz and the lattice vector defined above
    xyz_file = xyz_path

    file = open(xyz_file, 'r')
    coord_rec = open(xdatacar_path + '_unwrapped.xyz', 'w')

    origin_list = []  # Stores the origin as [element,[coords]]
    prev_list = []  # Stores the wrapped previous step
    unwrap_list = []  # Stores the instantaneous unwrapped

    element_list = []  # element list
    element_dict = {}  # number of elements stored

    content = file.readline()
    N = int(content)

    file.readline()
    step = 0

    while True:
        step += 1
        # Get and store the origin coordinates in origin_dict at first step
        if step == 1:
            for i in range(N):
                t = file.readline().rstrip('\n').split()
                element = t[0]
                if element not in element_list:
                    element_list.append(element)
                if element not in element_dict:
                    element_dict[element] = 1.0
                else:
                    element_dict[element] += 1.0
                coords = np.array([float(s) for s in t[1:]])
                origin_list.append([element, coords])
            # Copy the first set of coordinates as prev_dict and unwrapped
            unwrap_list = deepcopy(origin_list)
            prev_list = deepcopy(origin_list)

        # Read wrapped coordinates into wrapped_dict
        content = file.readline()

        if len(content) == 0:
            break

        N = int(content)
        file.readline()
        wrap_list = []  # Erase the previous set of coordinates
        for i in range(N):
            t = file.readline().rstrip('\n').split()
            element = t[0]
            coords = np.array([float(s) for s in t[1:]])
            wrap_list.append([element, coords])

        coord_rec.write(str(N) + "\ncomment\n")

        # Unwrap coordinates
        for atom in range(N):
            coord_rec.write(wrap_list[atom][0])

            # decompose wrapped atom coordinates to onto lattice vectors:
            w1 = wrap_list[atom][1][0]
            w2 = wrap_list[atom][1][1]
            w3 = wrap_list[atom][1][2]

            # decompose prev atom coordinates to onto lattice vectors:
            p1 = prev_list[atom][1][0]
            p2 = prev_list[atom][1][1]
            p3 = prev_list[atom][1][2]

            # get distance between periodic images and use the smallest one
            if np.fabs(w1 - p1) > 0.5 * L[0][0]:
                u1 = w1 - p1 - L[0][0] * np.sign(w1/L[0][0] - p1/L[0][0])
            else:
                u1 = w1 - p1

            if np.fabs(w2 - p2) > 0.5 * L[1][1]:
                u2 = w2 - p2 - L[1][1] * np.sign(w2/L[1][1] - p2/L[1][1])
            else:
                u2 = w2 - p2

            if np.fabs(w3 - p3) > 0.5 * L[2][2]:
                u3 = w3 - p3 - L[2][2] * np.sign(w3/L[2][2] - p3/L[2][2])
            else:
                u3 = w3 - p3

            # add unwrapped displacements to unwrapped coords
            unwrap_list[atom][1][0] += u1
            unwrap_list[atom][1][1] += u2
            unwrap_list[atom][1][2] += u3

            L_1 = np.eye(3)
            uw = unwrap_list[atom][1][0] * L_1[0] + unwrap_list[atom][1][1] * L_1[1] + unwrap_list[atom][1][2] * L_1[2]
            coord_rec.write(" " + np.array_str(uw).replace("[", "").replace("]", ""))
            coord_rec.write("\n")

        prev_list = deepcopy(wrap_list)

    file.close()
    coord_rec.close()



