import pandas as pd
from xdatbus.utils import gauss_pot


def calculate_profile_1d(hillspot_path, hills_count, cv_range, resolution=1000):
    """
    Calculate the 1D free energy profile from a HILLSPOT file.

        Parameters
        ----------
        hillspot_path : str
            The path of the HILLSPOT file
        hills_count : int
            The number of hills to be read
        cv_range : list
            The range of the collective variable
        resolution : int (optional)
            The resolution of the free energy profile
    """

    f = open(hillspot_path, "r")

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
        if step > hills_count:
            break
    f.close()

    step = (cv_range[1] - cv_range[0]) / resolution
    cv = cv_range[0]

    data_list = []

    for i in range(1, resolution):
        en = 0.0
        cv = cv + step
        for j in range(len(data)):
            cv0 = data[j][0]
            en_ = gauss_pot(cv, cv0, h[j], w[j])
            en += en_
        data_list.append({"cv": cv, "potential_energy": en})

    df = pd.DataFrame(data_list)

    return df


input_line_number = 10
fes = calculate_profile_1d(
    "../tests/data/hillspot/HILLSPOT_1D",
    input_line_number,
    cv_range=[6, 10],
    resolution=1000,
)
# plot the free energy profile
from matplotlib import pyplot as plt

plt.plot(fes["cv"], fes["potential_energy"])
plt.xlabel("CV")
plt.ylabel("Potential Energy")

plt.show()
