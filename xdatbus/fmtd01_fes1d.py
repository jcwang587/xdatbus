import numpy as np
import pandas as pd


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


def calculate_profile_1d(hillspot_path, input_line_number, xmin=8, xmax=10, num=1000):
    """
    Calculate the 1D free energy profile from a HILLSPOT file.
    """
    f = hillspot_path
    ff = f + ".xyz"

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
    step = (xmax - xmin) / num
    x = xmin

    # initialize a dataframe to store the potential energy with the x position
    df = pd.DataFrame(columns=["x", "potential_energy"])

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


hillspot_path = "../tests/data/hillspot/HILLSPOT"
input_line_number = 10
data = calculate_profile_1d(hillspot_path, input_line_number)
