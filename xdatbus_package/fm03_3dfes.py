import numpy as np


def gaussian_3d(x, y, z, center, height, width):
    cx, cy, cz = center
    return height * np.exp(-((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) / (2 * width ** 2))


def total_value_at_point(x, y, z, gaussians):
    total_value = 0.0
    for g in gaussians:
        total_value += gaussian_3d(x, y, z, g['center'], g['height'], g['width'])
    return total_value


def generate_cube_file_vesta(filename, origin, n_points, spacing, gaussians):
    with open(filename, 'w') as f:
        f.write("Gaussian Cube file for VESTA with multiple spheres\n")
        f.write("3D Gaussian functions\n")

        # Atom block
        f.write("0 {0:.6f} {1:.6f} {2:.6f}\n".format(origin[0], origin[1], origin[2]))

        # Voxel grid
        for i, (n, s) in enumerate(zip(n_points, spacing)):
            vector = [0.0, 0.0, 0.0]
            vector[i] = s * n
            f.write("{0} {1:.6f} {2:.6f} {3:.6f}\n".format(n, *vector))

        # Volumetric data
        for i in range(n_points[0]):
            for j in range(n_points[1]):
                for k in range(n_points[2]):
                    x = origin[0] + i * spacing[0]
                    y = origin[1] + j * spacing[1]
                    z = origin[2] + k * spacing[2]
                    val = total_value_at_point(x, y, z, gaussians)
                    f.write("{0:.6e} ".format(val))
                f.write("\n")
