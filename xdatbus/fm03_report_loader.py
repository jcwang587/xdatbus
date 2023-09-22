import os
import shutil


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

    # Extract the values from the first report file to determine the number of 'fic_p>' lines
    fic_p_count = 0
    with open(os.path.join(local_report_files_raw, report_files[0]), 'r') as file:
        in_metadynamics_section = False
        for line in file:
            if '>Metadynamics' in line:
                in_metadynamics_section = True
            elif in_metadynamics_section and 'fic_p>' in line:
                fic_p_count += 1
            elif in_metadynamics_section and not line.strip():  # empty line, end of metadynamics section
                break

    # Here, the fic_p_count variable holds the number of 'fic_p>' lines in a typical report
    print(f"Number of fic_p> lines: {fic_p_count}")

    fic_p_values = np.zeros((len(report_files), fic_p_count))

    # Extract the values from each line containing 'fic_p>'
    for idx, report_file in enumerate(report_files):
        temp_values = []
        with open(os.path.join(local_report_files_raw, report_file), 'r') as file:
            for line in file:
                if 'fic_p>' in line:
                    value = float(line.split()[-1])  # assumes value is the last item in the line
                    temp_values.append(value)

        # Insert values into the array
        fic_p_values[idx, :] = temp_values

    if delete_intermediate_folders:
        shutil.rmtree(local_report_files_raw)

    return fic_p_values
