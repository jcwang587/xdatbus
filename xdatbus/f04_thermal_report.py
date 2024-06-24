import os
import re
import argparse
from rich.console import Console
from rich.progress import Progress
from xdatbus.utils import filter_files
from pymatgen.io.vasp.outputs import Oszicar


def thermal_report(osz_dir="./", output_path="./", show_progress=False):
    """
    Generate a thermal report from the OSZICAR files.

        Parameters
        ----------
        osz_dir : str
            Input path of the OSZICAR files
        output_path : str
            Output path of the thermal report
        show_progress : bool
            Whether to show the progress bar
    """

    console = Console(log_path=False)

    try:
        raw_list = os.listdir(osz_dir)
        oszicar_list = filter_files(raw_list, "OSZICAR")

        if len(oszicar_list) == 0:
            raise ValueError("No OSZICAR file found in the directory.")
        elif len(oszicar_list) == 1:
            oszicar_list_sort = oszicar_list
        else:
            oszicar_list_sort = sorted(
                oszicar_list, key=lambda x: int(re.findall(r"\d+", x)[0])
            )

        console.log(f"sequence: {oszicar_list_sort}")

        potential_energy = []
        kinetic_energy = []
        total_energy = []
        temperature = []
        with Progress(console=console) as progress:
            if show_progress:
                task = progress.add_task(
                    "🚌 xdatbus thermal_report", total=len(oszicar_list_sort)
                )
            else:
                task = progress.add_task("🚌 xdatbus thermal_report", visible=False)

            for oszicar_file in oszicar_list_sort:
                console.log(f"thermal_report: Processing {oszicar_file}")
                progress.update(task, advance=1)
                oszicar_path = os.path.join(osz_dir, oszicar_file)
                oszicar = Oszicar(oszicar_path)
                for ionic_step in oszicar.ionic_steps:
                    potential_energy.append(ionic_step["E0"])
                    kinetic_energy.append(ionic_step["EK"])
                    total_energy.append(ionic_step["E"])
                    temperature.append(ionic_step["T"])

        csv_path = os.path.join(output_path, "thermal_report.csv")
        with open(csv_path, "w") as f:
            f.write("potential_energy,kinetic_energy,total_energy,temperature\n")
            for i in range(len(potential_energy)):
                f.write(
                    f"{potential_energy[i]},{kinetic_energy[i]},{total_energy[i]},{temperature[i]}\n"
                )

    except Exception as e:
        console.log(e)
        console.log("🚌 xdatbus thermal_report: Failed!")


def main():
    parser = argparse.ArgumentParser(description="Thermal report generator")

    parser.add_argument(
        "--osz_dir",
        type=str,
        default="./",
        help="The directory containing the OSZICAR files.",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        default="./",
        help="The directory to save the thermal report.",
    )

    args = parser.parse_args()

    thermal_report(args.osz_dir, args.output_path, show_progress=True)


if __name__ == "__main__":
    main()
