import os
import shutil
import matplotlib.pyplot as plt
import numpy as np


def gauss_pot(x: np.ndarray, x0: float, height: float, width: float) -> np.ndarray:
    """
    Calculate the Gaussian potential energy.

    Parameters:
    - x (np.ndarray): Array of positions at which to evaluate the potential.
    - x0 (float): The position of the potential minimum.
    - height (float): The height of the Gaussian potential.
    - width (float): The standard deviation (controls the width of the Gaussian).

    Returns:
    - np.ndarray: The potential energy at each position x.
    """
    en = height * np.exp(-((x - x0) ** 2) / (2.0 * width**2))
    return en


def calculate_profile_1d(hillspot_path, input_line_number, xmin=-1.0, xmax=2.0, num=1000):
    """
    Calculate the 1D free energy profile from a HILLSPOT file.
    """
    f = hillspot_path
    ff = f + ".xyz"

    a0 = 8
    a1 = 10.0
    num = 1000

    f = open(f, "r")

    data = []
    h = []
    w = []
    step = 0
    for line in f.readlines():
        line = line.split()
        x = []
        if len(line) > 2:
            for i in range(len(line) - 2):
                x.append(float(line[i]))
            data.append(x)
            h.append(float(line[-2]))
            w.append(float(line[-1]))
        step += 1
        if step > input_line_number:
            break
    f.close()

    ff = open(ff, "w")
    step = (a1 - a0) / num
    x = a0
    for i in range(1, num):
        en = 0.0
        x = x + step
        for j in range(len(data)):
            x0 = data[j][0]
            en_ = gauss_pot(x, x0, h[j], w[j])
            en += en_
        ff.write(repr(x) + "\t" + repr(-en) + "\n")
    ff.close()

    return data


def plot_profile(hillspot_path):
    # get the length of hillspot file
    f = hillspot_path
    f = open(f, "r")
    input_line_number = 0
    for _ in f.readlines():
        input_line_number += 1
    print("input_line_number = ", input_line_number)

    # calculate the profile
    fes = calculate_profile_1d(hillspot_path, input_line_number)
    fes = sum(fes, [])
    fes = np.array(fes)
    fes = fes.reshape(-1, 2)
    return fes


def plot_cv(hillspot_path, idx):
    # get the length of hillspot file
    f = hillspot_path
    f = open(f, "r")
    input_line_number = 0
    for _ in f.readlines():
        input_line_number += 1
    print("input_line_number = ", input_line_number)

    # calculate the profile
    cv = calculate_profile_1d(hillspot_path, input_line_number)
    cv = sum(cv, [])
    print(cv)
    # plot the cv
    plt.plot([float(x) * 200 / 1000 for x in range(len(cv))], cv, "-")
    if idx == 3:
        plt.xlabel("Time (ps)")
    plt.ylabel("CV")


hillspot_path = "../tests/data/hillspot/HILLSPOT"
hillspotxyz_plot = plot_profile(hillspot_path)
plt.plot(hillspotxyz_plot[:, 0], hillspotxyz_plot[:, 1], "-")
plt.xlabel("CV")
plt.ylabel("Free Energy (kcal/mol)")
plt.show()
plt.close()
