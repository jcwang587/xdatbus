import numpy as np
from scipy.ndimage import minimum_filter
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt


def neb_2d(fes, minima_1, minima_2, n_images, n_steps, spring_constant):
    # Create a regular grid to interpolate
    x = np.arange(fes.shape[0])
    y = np.arange(fes.shape[1])
    interpolator = RegularGridInterpolator((x, y), fes)

    # Initialize path using linear interpolation between minima
    path = np.vstack(
        [
            np.linspace(minima_1[0], minima_2[0], n_images),
            np.linspace(minima_1[1], minima_2[1], n_images),
        ]
    ).T

    # Store initial positions in path coordinates
    path_coords = path.copy()
    path_fes = interpolator(path_coords)

    for step in range(n_steps):
        new_path_coords = path_coords.copy()
        for i in range(1, n_images - 1):  # Exclude the first and last point
            # Compute tangential (spring) forces
            tau = path_coords[i + 1] - path_coords[i - 1]
            tau_norm = np.linalg.norm(tau)
            if tau_norm != 0:
                tau /= tau_norm

            # Calculate spring forces
            f_spring = spring_constant * (
                (
                    np.linalg.norm(path_coords[i + 1] - path_coords[i])
                    - np.linalg.norm(path_coords[i] - path_coords[i - 1])
                )
                * tau
            )

            # Evaluate the potential energy surface at current path point
            fes_val = interpolator(path_coords[i])
            # Calculate gradient using finite differences around the path point
            eps = 1e-5  # a small perturbation
            grad_x = (interpolator(path_coords[i] + [eps, 0]) - fes_val) / eps
            grad_y = (interpolator(path_coords[i] + [0, eps]) - fes_val) / eps
            gradient = np.array([grad_x, grad_y])

            # Perpendicular component of the gradient
            gradient = gradient.flatten()
            f_perp = gradient - np.dot(gradient, tau) * tau

            # Update the image position
            new_path_coords[i] += -f_perp + f_spring

            # Ensure the new path point stays within bounds
            new_path_coords[i] = np.clip(
                new_path_coords[i], [0, 0], np.array(fes.shape) - 1
            )

        path_coords = new_path_coords

        path_fes = interpolator(path_coords)

    return path_coords, path_fes


# Load your FES data
fes = np.load("../tests/data/npy/y_fes_300k.npy")


def find_local_minima(data):
    filtered_data = minimum_filter(data, size=3, mode="constant", cval=np.inf)
    local_minima = data == filtered_data
    local_minima_coords = np.argwhere(local_minima)
    return local_minima_coords


def main():
    local_minima_coords = find_local_minima(fes)
    n_images = 10
    n_steps = 10000
    spring_constant = 0.5

    mep, mep_fes = neb_2d(
        fes,
        local_minima_coords[1],
        local_minima_coords[3],
        n_images,
        n_steps,
        spring_constant,
    )

    # plot the minimum energy path
    plt.imshow(fes, cmap="viridis")
    plt.plot(mep[:, 1], mep[:, 0], "ro-")
    plt.xlabel("Reaction coordinate 1")
    plt.ylabel("Reaction coordinate 2")
    for i, (x, y) in enumerate(local_minima_coords):
        plt.text(y, x, f"{i}", color="red")
    plt.colorbar()
    plt.show()

    # Output the FES values along the MEP
    print("FES values along the MEP:", mep_fes)

    plt.figure()
    plt.plot(mep_fes, "r-")
    plt.xlabel("Image Number")
    plt.ylabel("FES Value (kJ/mol)")
    plt.title("FES Profile Along MEP")
    plt.grid(True)
    plt.show()