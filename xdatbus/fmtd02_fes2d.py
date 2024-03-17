import pandas as pd
from xdatbus.utils import gauss_pot_2d


def fes_2d(hillspot_path, hills_count, cv_1_range, cv_2_range, resolution=100):
    """
    Calculate the 2D free energy profile from a HILLSPOT file.

        Parameters
        ----------
        hillspot_path : str
            The path of the HILLSPOT file
        hills_count : int
            The number of hills to be read
        cv_1_range : list
            The range of the first collective variable
        cv_2_range : list
            The range of the second collective variable
        resolution : int (optional)
            The resolution of the free energy profile
    """
    assert (
        isinstance(cv_1_range, list) and len(cv_1_range) == 2
    ), "cv_1_range must be a list of length 2"
    assert (
        isinstance(cv_2_range, list) and len(cv_2_range) == 2
    ), "cv_2_range must be a list of length 2"

    f = open(hillspot_path, "r")

    data = []
    h = []
    w = []
    hills_in = 0
    for line in f.readlines():
        line = line.split()
        x = []
        if len(line) > 2:
            for i in range(len(line) - 2):
                x.append(float(line[i]))
            data.append(x)
            h.append(float(line[-2]))
            w.append(float(line[-1]))
        hills_in += 1
        if hills_in > hills_count:
            break
    f.close()

    step_1 = (cv_1_range[1] - cv_1_range[0]) / resolution
    step_2 = (cv_2_range[1] - cv_2_range[0]) / resolution
    cv_1 = cv_1_range[0]

    data_list = []

    for i in range(1, resolution):
        cv_1 = cv_1 + step_1
        cv_2 = cv_2_range[0]
        for k in range(1, resolution):
            en = 0.0
            cv_2 = cv_2 + step_2
            for j in range(len(data)):
                cv_1_0 = data[j][0]
                cv_2_0 = data[j][1]
                en_ = gauss_pot_2d(cv_1, cv_2, cv_1_0, cv_2_0, h[j], w[j])
                en += en_
            data_list.append({"cv_1": cv_1, "cv_2": cv_2, "potential_energy": en})

    df = pd.DataFrame(data_list)

    return df
