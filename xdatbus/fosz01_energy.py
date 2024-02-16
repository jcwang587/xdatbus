import os
import re
from xdatbus.utils import filter_files
from pymatgen.io.vasp.outputs import Oszicar


def energy_report(osz_dir="./", output_path="./"):
    try:
        raw_list = os.listdir(osz_dir)
        oszicar_list = filter_files(raw_list, "OSZICAR")

        if len(oszicar_list) == 0:
            raise ValueError("No OSZICAR file found in the directory.")

        oszicar_list_sort = sorted(
            oszicar_list, key=lambda x: int(re.findall(r"\d+", x)[0])
        )

        # load energy
        for oszicar_file in oszicar_list_sort:
            oszicar_path = os.path.join(osz_dir, oszicar_file)
            oszicar = Oszicar(oszicar_path)
            energy = oszicar.ionic_steps[:]

            print(energy)

        print("xdatbus-func | energy_report: Done!")

    except Exception as e:
        print(e)
        print("xdatbus-func | energy_report: Failed!")


energy_report()


