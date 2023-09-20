import os
import shutil


def f03_report_loader(
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
        load_pre_xdatcar : bool (optional)
            If ``True``, the trajectory will contain the previous frames (before the current run)
        load_last_xdatcar : bool (optional)
            If ``True``, the trajectory will contain the last frame
        delete_intermediate_folders : bool (optional)
            If ``True``, the intermediate folders will be deleted
    """

    # Define the path to the XDATCAR file
    remote_file_list = os.listdir(aimd_path)
    run_list = [run for run in remote_file_list if 'RUN' in run]
    # sort run_list by the number in the run name
    run_list.sort(key=lambda x: int(x[3:]))
    xdatcar_path_list = [aimd_path + "/" + run_list[i] + "/REPORT" for i in range(len(run_list))]
    print('analyze the following REPORT files:')
    print(xdatcar_path_list)

    local_report_files_raw = "./report_files_raw"
    local_report_files_wrap = "./report_files_wrap"

    # Clear the directory
    if os.path.exists(local_report_files_raw):
        shutil.rmtree(local_report_files_raw)
    os.mkdir(local_report_files_raw)


    if delete_intermediate_folders:
        shutil.rmtree(local_report_files_raw)

    print("Done.")
