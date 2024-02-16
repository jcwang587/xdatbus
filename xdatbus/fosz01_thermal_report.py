import os
import re
import argparse
from xdatbus.utils import filter_files
from pymatgen.io.vasp.outputs import Oszicar


def thermal_report(osz_dir="./", output_path="./"):
    try:
        raw_list = os.listdir(osz_dir)
        oszicar_list = filter_files(raw_list, "OSZICAR")

        if len(oszicar_list) == 0:
            raise ValueError("No OSZICAR file found in the directory.")

        oszicar_list_sort = sorted(
            oszicar_list, key=lambda x: int(re.findall(r"\d+", x)[0])
        )

        potential_energy = []
        kinetic_energy = []
        total_energy = []
        temperature = []
        for oszicar_file in oszicar_list_sort:
            print(f"xdatbus-func | energy_report: Processing {oszicar_file}")
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

        print("xdatbus-func | energy_report: Done!")

    except Exception as e:
        print(e)
        print("xdatbus-func | energy_report: Failed!")


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

    thermal_report(args.osz_dir, args.output_path)


if __name__ == "__main__":
    main()
