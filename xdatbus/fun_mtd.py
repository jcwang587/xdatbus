import pandas as pd
import numpy as np
from xdatbus.utils import gauss_pot_1d
from xdatbus.utils import gauss_pot_2d
from xdatbus.utils import gauss_pot_3d
import os
import shutil
from ase.io import read, write
from MDAnalysis import Universe
from MDAnalysis.coordinates.XTC import XTCWriter
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.ndimage import minimum_filter
from scipy.interpolate import RegularGridInterpolator


def fes_1d(hillspot_path, hills_count, cv_range, resolution=100):
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
    assert (
        isinstance(cv_range, list) and len(cv_range) == 2
    ), "cv_range must be a list of length 2"

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

    step = (cv_range[1] - cv_range[0]) / resolution
    cv = cv_range[0]

    data_list = []

    for i in range(1, resolution):
        en = 0.0
        cv = cv + step
        for j in range(len(data)):
            cv0 = data[j][0]
            en_ = gauss_pot_1d(cv, cv0, h[j], w[j])
            en += en_
        data_list.append({"cv": cv, "potential_energy": en})

    df = pd.DataFrame(data_list)

    return df


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


def hillspot2hills(
    hillspot_dir,
    hills_dir,
    cv,
    height_conversion=1,
    sigma_conversion=1,
    del_inter=False,
):
    """
    Convert HILLSPOT file to HILLS file
        Parameters
        ----------
        hillspot_dir : str
            Path to HILLSPOT file
        hills_dir : str
            Path to the directory where the HILLS file will be created
        cv : str or list
            Name of the collective variable(s)
        height_conversion : float(optional)
            Conversion factor to convert the unit of the height from eV to kJ/mol
        sigma_conversion : float(optional)
            Conversion factor to convert the unit of the sigma based on the lattice in Angstrom
        del_inter : bool(optional)
            Delete the intermediate files created by this function.
    """
    hillspot = open(hillspot_dir, "r")
    column_names = (cv if isinstance(cv, list) else [cv]) + ["height", "sigma"]
    hs = pd.read_csv(hillspot, sep="\s+", header=None, names=column_names)

    hs["time"] = range(1, len(hs) + 1)
    hs["bias_factor"] = -1

    hs["sigma"] = hs["sigma"] * sigma_conversion
    hs["height"] = hs["height"] * height_conversion

    if isinstance(cv, list):
        for variable in cv:
            hs[variable] = hs[variable] * sigma_conversion
            # Create new sigma column for each CV
            hs["sigma_" + variable] = hs["sigma"] * sigma_conversion
        # Drop the old 'sigma' column as we have created new ones for each CV
        hs.drop(columns="sigma", inplace=True)
    else:
        hs[cv] = hs[cv] * sigma_conversion
        hs["sigma_" + cv] = hs["sigma"] * sigma_conversion

    # Generate the header
    header_str = "#! FIELDS time "
    for variable in cv if isinstance(cv, list) else [cv]:
        header_str += variable + " "
    for variable in cv if isinstance(cv, list) else [cv]:
        header_str += "sigma_" + variable + " "
    header_str += "height biasf\n"

    # Create the order for columns
    order = ["time"] + (cv if isinstance(cv, list) else [cv])
    for variable in cv if isinstance(cv, list) else [cv]:
        order.append("sigma_" + variable)
    order += ["height", "bias_factor"]
    hs = hs[order]

    # write the dataframe to a hills file with tab-separated format
    hs.to_csv("HILLS", sep="\t", header=False, index=False, float_format="%.4f")

    file = open("HILLS", "r+")
    lines = file.readlines()
    file.seek(0, 0)
    file.write(header_str)
    file.write("#! SET multivariate " + str(isinstance(cv, list)).lower() + "\n")
    for line in lines:
        file.write(line)
    file.close()

    # copy the HILLS file to the hills_dir
    if hills_dir != "HILLS":
        shutil.copy("HILLS", hills_dir)
        print("HILLS file is copied to", hills_dir)
    else:
        print("HILLS file is created in the current directory.")

    # delete the intermediate files
    if del_inter:
        os.remove("HILLS")
        print("Intermediate files are deleted.")


def report_loader(
    aimd_path,
    load_pre_report=True,
    load_last_report=False,
    delete_intermediate_folders=True,
):
    """
    Initialize a trajectory writer instance for *filename*.

        Parameters
        ----------
        aimd_path : str
            Output filename of the trajectory; the extension determines the format.
        load_pre_report : bool (optional)
            If ``True``, the trajectory will contain the previous frames (before the current run)
        load_last_report : bool (optional)
            If ``True``, the trajectory will contain the last frame
        delete_intermediate_folders : bool (optional)
            If ``True``, the intermediate folders will be deleted
    """

    # Define the path to the REPORT file
    remote_file_list = os.listdir(aimd_path)
    run_list = [run for run in remote_file_list if "RUN" in run]
    # sort run_list by the number in the run name
    run_list.sort(key=lambda x: int(x[3:]))
    report_path_list = [
        aimd_path + "/" + run_list[i] + "/REPORT" for i in range(len(run_list))
    ]
    print("analyze the following REPORT files:")
    print(report_path_list)

    local_report_files_raw = "./report_files_raw"

    # Clear the directory
    if os.path.exists(local_report_files_raw):
        shutil.rmtree(local_report_files_raw)
    os.mkdir(local_report_files_raw)

    # Copy the REPORT file to the current directory
    print("Copying REPORT files to the current directory ...")
    i = 0
    if load_pre_report:
        for i in range(len(report_path_list)):
            shutil.copy(
                report_path_list[i],
                local_report_files_raw + "/" + "REPORT_" + str(i + 1).zfill(5),
            )
    if load_last_report:
        report_path_last = aimd_path + "/REPORT"
        print(report_path_last)
        if load_pre_report:
            shutil.copy(
                report_path_last,
                local_report_files_raw + "/" + "REPORT_" + str(i + 2).zfill(5),
            )
        else:
            shutil.copy(
                report_path_last,
                local_report_files_raw + "/" + "REPORT_" + str(i + 1).zfill(5),
            )

    # Load the REPORT file
    print("Loading REPORT files ...")
    report_files = os.listdir(local_report_files_raw)

    all_reports_fic_p_values = []  # This will be a list of lists

    # Extract the values from each line containing 'fic_p>'
    for report_file in report_files:
        with open(os.path.join(local_report_files_raw, report_file), "r") as file:
            current_report_fic_p_values = (
                []
            )  # to store the fic_p values for a specific MD step
            for line in file:
                if "fic_p>" in line:
                    value = float(
                        line.split()[-1]
                    )  # assumes value is the last item in the line
                    current_report_fic_p_values.append(value)
                if "MD step No." in line and current_report_fic_p_values:
                    all_reports_fic_p_values.append(current_report_fic_p_values)
                    current_report_fic_p_values = []

            # In case the file ends and there's no more 'MD step No.' after the last 'fic_p>'
            if current_report_fic_p_values:
                all_reports_fic_p_values.append(current_report_fic_p_values)

    # Determine the number of fic_p> lines by looking at the maximum length of sub-lists
    num_fic_p_lines = max(map(len, all_reports_fic_p_values))

    # Create a numpy array with dynamic shape based on number of fic_p> lines
    shape = [len(all_reports_fic_p_values)] + [num_fic_p_lines]
    fic_p_array = np.zeros(shape)
    for i, fic_p_values in enumerate(all_reports_fic_p_values):
        for j, value in enumerate(fic_p_values):
            fic_p_array[i, j] = value

    if delete_intermediate_folders:
        shutil.rmtree(local_report_files_raw)

    return fic_p_array


def xdc2xtc(xdc_path):
    """
    Convert a VASP XDATCAR file to an XTC trajectory file.

    Parameters
    ----------
    xdc_path : str
        Path to the XDATCAR file
    """
    # Load XDATCAR using ASE and write to a temporary XYZ file
    xdatcar = read(xdc_path, format="vasp-xdatcar", index=":")
    temp_xyz_path = xdc_path + ".xyz"
    xtc_path = xdc_path + ".xtc"

    with open(temp_xyz_path, "w") as file:
        write(file, xdatcar, format="xyz")

    # close the file
    file.close()

    # Initialize MDAnalysis Universe
    u = Universe(temp_xyz_path)

    # Write out the XTC file
    with XTCWriter(xtc_path, n_atoms=u.atoms.n_atoms) as w:
        for ts in u.trajectory:
            print(f"Writing frame {ts.frame}")
            w.write(u.atoms)


def reweight(fes, cv, nv, kb, t, grid_min, grid_max, grid_num):
    """Reweight a metadynamics simulation to the unbiased ensemble using histogram reweighting.

    In many cases you might decide which variable should be analyzed after having performed a metadynamics simulation.
    For example, you might want to calculate the free energy as a function of CVs other than those biased during the
    metadynamics simulation. At variance with standard MD simulations, you cannot simply calculate histograms of other
    variables directly from your metadynamics trajectory, because the presence of the metadynamics bias potential has
    altered the statistical weight of each frame. To remove the effect of this bias and thus be able to calculate properties
    of the system in the unbiased ensemble, you must reweight (unbias) your simulation.

        Parameters
        ----------
        fes : np.ndarray
            The free energy surface calculated from the metadynamics simulation.
        cv : np.ndarray
            The collective variable used in the metadynamics simulation.
        nv : np.ndarray
            The new collective variable for which the potential of mean force will be calculated.
        kb : float
            The Boltzmann constant.
        t : float
            The temperature of the simulation.
        grid_min : float
            The minimum value of the collective variable.
        grid_max : float
            The maximum value of the collective variable.
        grid_num : int
            The number of bins in the histogram.

    Returns
    -------
    np.ndarray
        The unbiased free energy surface.
    """
    fes_flat = fes.flatten()
    cv_hist = np.exp(-fes_flat / (kb * t))

    nv_bins = np.linspace(grid_min, grid_max, grid_num)
    nv_hist = np.zeros(len(nv_bins) - 1)

    for i in range(len(nv)):
        for j in range(len(cv_hist)):
            if nv_bins[i] <= nv[j] < nv_bins[i + 1]:
                nv_hist[i] += cv_hist[j]

    nv_hist = nv_hist / np.sum(nv_hist)

    pmf = -kb * t * np.log(nv_hist)
    pmf -= np.min(pmf)

    pmf_smooth = lowess(pmf, nv_bins, frac=0.1, return_sorted=False)

    return pmf_smooth


def pmf_321(fes3d, axis1, axis2):
    """project 3d free energy surface to 1d

    Parameters
    ----------
    fes3d : np.ndarray
        The 3d free energy surface.
    axis1 : int
        The axis to be projected.
    axis2 : int
        The axis to be projected.

    Returns
    -------
    np.ndarray
        The 2d free energy surface.
    """

    fes2d = np.sum(fes3d, axis=axis1)
    fes1d = np.sum(fes2d, axis=axis2)

    return fes1d


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


def local_minima(data, size=3):
    filtered_data = minimum_filter(data, size=size, mode="constant", cval=np.inf)
    minima = data == filtered_data
    minima_coords = np.argwhere(minima)
    return minima_coords
