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

    step = (xmax - xmin) / num
    x = xmin

    # Initialize a list to store dictionaries
    data_list = []

    for i in range(1, num):
        en = 0.0
        x = x + step
        for j in range(len(data)):
            x0 = data[j][0]
            en_ = gauss_pot(x, x0, h[j], w[j])
            en += en_
        # Append data to the list
        data_list.append({"x": x, "potential_energy": en})

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data_list)

    return df


hillspot_path = "../tests/data/hillspot/HILLSPOT"
input_line_number = 10
data = calculate_profile_1d(hillspot_path, input_line_number)