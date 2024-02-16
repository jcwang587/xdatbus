import os
import re
import shutil
import argparse
from ase.io import read, write
from pymatgen.io.vasp.outputs import Xdatcar
from xdatbus.utils import update_folder, remove_file, filter_files


def xdc_aggregate(xdc_dir="./", output_path="./", delete_temp_files=True):
    """
    Initialize a trajectory writer instance for *filename*.

        Parameters
        ----------
        xdc_dir : str
            Input path of the AIMD simulation, which contains the XDATCAR files
        output_path : str (optional)
            Output path of the XDATBUS file
        delete_temp_files : bool (optional)
            If ``False``, the intermediate folders will be deleted
    """
    try:
        raw_list = os.listdir(xdc_dir)
        xdatcar_list = filter_files(raw_list, "XDATCAR")

        if len(xdatcar_list) == 0:
            raise ValueError("No XDATCAR file found in the directory.")

        xdatcar_list_sort = sorted(
            xdatcar_list, key=lambda x: int(re.findall(r"\d+", x)[0])
        )

        xdatcar_wrap_path = os.path.join(output_path, "XDATCAR_wrap")
        xdatbus_path = os.path.join(output_path, "XDATBUS")
        log_path = os.path.join(output_path, "xdc_aggregate.log")

        # Clear the directory
        update_folder(xdatcar_wrap_path)

        # Remove the XDATBUS and log files
        remove_file(xdatbus_path)
        remove_file(log_path)

        log_file = open(log_path, "w")
        for xdatcar_raw in xdatcar_list_sort:
            print("xdatbus-func | xdc_aggregate: Wrapping " + xdatcar_raw + " ...")
            xdatcar = read(
                xdc_dir + "/" + xdatcar_raw, format="vasp-xdatcar", index=":"
            )
            print(
                "xdatbus-func | xdc_aggregate: number of frames: " + str(len(xdatcar))
            )
            write(
                xdatcar_wrap_path + "/" + xdatcar_raw,
                format="vasp-xdatcar",
                images=xdatcar,
            )
            log_file.write(xdatcar_raw + " " + str(len(xdatcar)) + "\n")
        log_file.close()

        # Get the number of files in wrap directory
        wrap_list = os.listdir(xdatcar_wrap_path)
        wrap_list_sort = sorted(wrap_list, key=lambda x: int(re.findall(r"\d+", x)[0]))

        # Combine the wrapped XDATCAR files into one XDATCAR file (XDATBUS) using pymatgen
        xdatbus = Xdatcar(xdatcar_wrap_path + "/" + wrap_list_sort[0])

        for xdatcar_wrap in wrap_list_sort[1:]:
            print("xdatbus-func | xdc_aggregate: Appending " + xdatcar_wrap + " ...")
            xdatcar = Xdatcar(xdatcar_wrap_path + "/" + xdatcar_wrap)
            xdatbus.structures.extend(xdatcar.structures)
        xdatbus.write_file(xdatbus_path)

        if delete_temp_files:
            shutil.rmtree(xdatcar_wrap_path)
            os.remove(log_path)

        print("sequence: ", xdatcar_list_sort)
        print("xdatbus-func | xdc_aggregate: Done!")

    except Exception as e:
        print(e)
        print("xdatbus-func | xdc_aggregate: Failed!")


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate XDATCAR files from an AIMD simulation."
    )
    parser.add_argument(
        "--xdc_dir",
        type=str,
        default="./",
        help="Input path of the AIMD simulation, which contains the XDATCAR files",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="./",
        help="Output path of the XDATBUS file (default: current directory)",
    )
    parser.add_argument(
        "--delete_temp_files",
        type=str,
        choices=["True", "False"],
        default="True",
        help="Choose True (default) to delete intermediate folders, or False to keep them.",
    )
    args = parser.parse_args()

    args.delete_temp_files = args.delete_temp_files == "True"

    xdc_aggregate(args.xdc_dir, args.output_path, args.delete_temp_files)


if __name__ == "__main__":
    main()
