import os
import shutil
import numpy as np


def fm03_report_loader(
        aimd_path,
        load_pre_report=True,
        load_last_report=False,
        delete_intermediate_folders=True
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
    run_list = [run for run in remote_file_list if 'RUN' in run]
    # sort run_list by the number in the run name
    run_list.sort(key=lambda x: int(x[3:]))
    report_path_list = [aimd_path + "/" + run_list[i] + "/REPORT" for i in range(len(run_list))]
    print('analyze the following REPORT files:')
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
            shutil.copy(report_path_list[i], local_report_files_raw + "/" + "REPORT_" + str(i + 1).zfill(5))
    if load_last_report:
        report_path_last = aimd_path + "/REPORT"
        print(report_path_last)
        if load_pre_report:
            shutil.copy(report_path_last, local_report_files_raw + "/" + "REPORT_" + str(i + 2).zfill(5))
        else:
            shutil.copy(report_path_last, local_report_files_raw + "/" + "REPORT_" + str(i + 1).zfill(5))

    # Load the REPORT file
    print("Loading REPORT files ...")
    report_files = os.listdir(local_report_files_raw)

    all_reports_fic_p_values = []  # This will be a list of lists

    # Extract the values from each line containing 'fic_p>'
    for report_file in report_files:
        with open(os.path.join(local_report_files_raw, report_file), 'r') as file:
            current_report_fic_p_values = []  # to store the fic_p values for a specific MD step
            for line in file:
                if 'fic_p>' in line:
                    value = float(line.split()[-1])  # assumes value is the last item in the line
                    current_report_fic_p_values.append(value)
                if 'MD step No.' in line and current_report_fic_p_values:
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