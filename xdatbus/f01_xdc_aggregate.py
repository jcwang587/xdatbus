import os
import re
import shutil
import argparse
from ase.io import read, write
from rich.console import Console
from rich.progress import Progress
from pymatgen.io.vasp.outputs import Xdatcar
from xdatbus.utils import update_folder, remove_file, filter_files


def xdc_aggregate(xdc_dir="./", output_dir="./", del_temp=True, show_progress=False):
    """
    Aggregate XDATCAR files from an AIMD simulation.

        Parameters
        ----------
        xdc_dir : str (optional)
            Input path of the AIMD simulation, which contains the XDATCAR files
        output_dir : str (optional)
            Output path of the XDATBUS file
        del_temp : bool (optional)
            If ``False``, the intermediate folders will be deleted
        show_progress : bool (optional)
            Whether to show the progress bar
    """

    console = Console(log_path=False)

    try:
        raw_list = os.listdir(xdc_dir)
        xdatcar_list = filter_files(raw_list, "XDATCAR")

        if len(xdatcar_list) == 0:
            raise ValueError("No XDATCAR file found in the directory.")
        elif len(xdatcar_list) == 1:
            xdatcar_list_sort = xdatcar_list
        else:
            xdatcar_list_sort = sorted(
                xdatcar_list, key=lambda x: int(re.findall(r"\d+", x)[0])
            )

        console.log(f"sequence: {xdatcar_list_sort}")

        xdatcar_wrap_path = os.path.join(output_dir, "XDATCAR_wrap")
        xdatbus_path = os.path.join(output_dir, "XDATBUS")

        # Clear the directory
        update_folder(xdatcar_wrap_path)

        # Remove the XDATBUS and log files
        remove_file(xdatbus_path)

        with Progress(console=console) as progress:
            if show_progress:
                task = progress.add_task(
                    "🚌 xdatbus xdc_aggregate", total=len(xdatcar_list_sort) * 2 + 1
                )
            else:
                task = progress.add_task("🚌 xdatbus xdc_aggregate", visible=False)
            for xdatcar_raw in xdatcar_list_sort:
                xdatcar = read(
                    xdc_dir + "/" + xdatcar_raw, format="vasp-xdatcar", index=":"
                )
                write(
                    xdatcar_wrap_path + "/" + xdatcar_raw,
                    format="vasp-xdatcar",
                    images=xdatcar,
                )
                progress.console.log(
                    f"xdc_aggregate: wrapping {xdatcar_raw} | number of frames: {len(xdatcar)}"
                )
                progress.update(task, advance=1)

            # Get the number of files in wrap directory
            wrap_list = os.listdir(xdatcar_wrap_path)
            wrap_list_sort = sorted(
                wrap_list, key=lambda x: int(re.findall(r"\d+", x)[0])
            )

            # Combine the wrapped XDATCAR files into one XDATCAR file (XDATBUS) using pymatgen
            xdatbus = Xdatcar(xdatcar_wrap_path + "/" + wrap_list_sort[0])

            progress.console.log(f"xdc_aggregate: initializing XDATBUS")
            progress.update(task, advance=1)

            for xdatcar_wrap in wrap_list_sort[1:]:
                xdatcar = Xdatcar(xdatcar_wrap_path + "/" + xdatcar_wrap)
                xdatbus.structures.extend(xdatcar.structures)
                progress.console.log(f"xdc_aggregate: appending {xdatcar_wrap}")
                progress.update(task, advance=1)

            xdatbus.write_file(xdatbus_path)
            progress.update(task, advance=1)

        if del_temp:
            shutil.rmtree(xdatcar_wrap_path)

    except Exception as e:
        console.log(e)
        console.log("🚌 xdatbus xdc_aggregate: Failed!")


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
        "--output_dir",
        type=str,
        default="./",
        help="Output path of the XDATBUS file (default: current directory)",
    )

    parser.add_argument(
        "--del_temp",
        type=str,
        choices=["True", "False"],
        default="True",
        help="Choose True (default) to delete intermediate folders, or False to keep them.",
    )

    args = parser.parse_args()

    args.del_temp = args.del_temp == "True"

    xdc_aggregate(args.xdc_dir, args.output_dir, args.del_temp, show_progress=True)


if __name__ == "__main__":
    main()
