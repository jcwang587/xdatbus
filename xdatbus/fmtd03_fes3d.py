import pandas as pd
from xdatbus.utils import gauss_pot_3d


def fes_3d(hillspot_path, hills_count, cv_1_range, cv_2_range, cv_3_range, resolution=50):
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
    assert isinstance(cv_1_range, list) and len(cv_1_range) == 2, "cv_1_range must be a list of length 2"
    assert isinstance(cv_2_range, list) and len(cv_2_range) == 2, "cv_2_range must be a list of length 2"
    assert isinstance(cv_3_range, list) and len(cv_3_range) == 2, "cv_3_range must be a list of length 2"

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
        cv_3 = cv_3_range[0]
        for k in range(1, resolution):
            cv_2 = cv_2 + step_2
            cv_3 = cv_3_range[0]
            for l in range(1, resolution):
                en = 0.0
                cv_3 = cv_3 + step_3
                for j in range(len(data)):
                    cv_1_0 = data[j][0]
                    cv_2_0 = data[j][1]
                    cv_3_0 = data[j][2]
                    en_ = gauss_pot_3d(cv_1, cv_2, cv_3, cv_1_0, cv_2_0, cv_3_0, h[j], w[j])
                    en += en_
                data_list.append({"cv_1": cv_1, "cv_2": cv_2, "cv_3": cv_3, "potential_energy": en})

    df = pd.DataFrame(data_list)

    return df


def main():
    fes = fes_3d(
        hillspot_path="../tests/data/hillspot/HILLSPOT_3D",
        hills_count=10,
        cv_1_range=[5, 10],
        cv_2_range=[5, 10],
        cv_3_range=[5, 10],
        resolution=100,
    )

    from matplotlib import pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(fes["cv_1"], fes["cv_2"], fes["potential_energy"], cmap="viridis")
    ax.set_xlabel("CV 1")
    ax.set_ylabel("CV 2")
    ax.set_zlabel("Potential Energy")
    plt.show()


if __name__ == "__main__":
    main()
