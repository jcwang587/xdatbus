import pandas as pd
from xdatbus.utils import gauss_pot_3d


def fes_3d(
    hillspot_path, hills_count, cv_1_range, cv_2_range, cv_3_range, resolution=100
):
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
        cv_3_range : list
            The range of the third collective variable
        resolution : int (optional)
            The resolution of the free energy profile
    """
    assert (
        isinstance(cv_1_range, list) and len(cv_1_range) == 2
    ), "cv_1_range must be a list of length 2"
    assert (
        isinstance(cv_2_range, list) and len(cv_2_range) == 2
    ), "cv_2_range must be a list of length 2"
    assert (
        isinstance(cv_3_range, list) and len(cv_3_range) == 2
    ), "cv_3_range must be a list of length 2"

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
    step_3 = (cv_3_range[1] - cv_3_range[0]) / resolution
    cv_1 = cv_1_range[0]

    data_list = []

    for i in range(1, resolution):
        cv_1 = cv_1 + step_1
        cv_2 = cv_2_range[0]
        for m in range(1, resolution):
            cv_2 = cv_2 + step_2
            cv_3 = cv_3_range[0]
            for n in range(1, resolution):
                en = 0.0
                cv_3 = cv_3 + step_3
                for j in range(len(data)):
                    cv_1_0 = data[j][0]
                    cv_2_0 = data[j][1]
                    cv_3_0 = data[j][2]
                    en_ = gauss_pot_3d(
                        cv_1, cv_2, cv_3, cv_1_0, cv_2_0, cv_3_0, h[j], w[j]
                    )
                    en += en_
                data_list.append(
                    {"cv_1": cv_1, "cv_2": cv_2, "cv_3": cv_3, "potential_energy": en}
                )

    df = pd.DataFrame(data_list)

    return df


from matplotlib import pyplot as plt
import numpy as np


def main():
    fes = fes_3d(
        hillspot_path="../tests/data/hillspot/HILLSPOT_3D",
        hills_count=9,
        cv_1_range=[5, 10],
        cv_2_range=[5, 10],
        cv_3_range=[5, 10],
        resolution=100,
    )

    # 1. Find the `cv_3` value closest to 7.
    unique_cv_3_values = fes["cv_3"].unique()
    closest_cv_3 = unique_cv_3_values[np.abs(unique_cv_3_values - 9).argmin()]

    # 2. Filter the DataFrame for the closest `cv_3` value.
    fes_closest = fes[fes["cv_3"] == closest_cv_3]

    # Ensure the DataFrame is not empty after filtering.
    if not fes_closest.empty:
        # 3. Pivot the DataFrame for plotting.
        fes_pivot = fes_closest.pivot(
            index="cv_1", columns="cv_2", values="potential_energy"
        )

        # Sorting the index to have a proper orientation in the plot.
        fes_pivot = fes_pivot.sort_index(ascending=False)

        # 4. Plotting
        plt.contourf(
            fes_pivot.columns, fes_pivot.index, fes_pivot.values, cmap="viridis"
        )
        plt.colorbar()
        plt.xlabel("cv_1")
        plt.ylabel("cv_2")
        plt.title(f"Free Energy Surface at cv_3 ~ {closest_cv_3}")
        plt.show()


if __name__ == "__main__":
    main()
