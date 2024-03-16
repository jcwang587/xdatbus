import argparse
import numpy as np
from rich.console import Console
from rich.progress import Progress
from pymatgen.io.vasp.outputs import Xdatcar
from xdatbus.utils import unwrap_pbc_dis


def xdc_unwrap(xdc_path="./XDATBUS", output_path="./XDATBUS_unwrap.xyz", show_progress=False):
    """
    Unwrap the coordinates in the XDATCAR file (to .xyz).

        Parameters
        ----------
        xdc_path : str
            Input path of the XDATCAR file
        output_path : str
            Output path of the xyz file
        show_progress : bool (optional)
            Show the progress bar or not
    """

    console = Console(log_path=False)

    try:
        xdatcar = Xdatcar(xdc_path)

        with Progress(console=console) as progress:
            if show_progress:
                task = progress.add_task(
                    "🚌 xdatbus xdc_unwrap", total=len(xdatcar.structures) // 100 + 1
                )
            else:
                task = progress.add_task("🚌 xdatbus xdc_unwrap", visible=False)

            # initialize an empty list to store unwrapped fractional coordinates
            unwrapped_coords = []

            # Initialize a variable to store the previously unwrapped coordinates
            previous_unwrapped_coords = xdatcar.structures[0].frac_coords

            unwrapped_coords.append(
                previous_unwrapped_coords.copy()
            )  # Store the first set of coordinates

            for i in range(1, len(xdatcar.structures)):  # Start from the second frame
                if (i + 1) % 100 == 0:
                    progress.console.log(f"xdc_unwrap: Processing step {i + 1}")
                    progress.update(task, advance=1)

                # initialize an empty array for the current structure's unwrapped coordinates
                current_unwrapped_coords = np.zeros_like(
                    xdatcar.structures[i].frac_coords
                )

                for j in range(len(xdatcar.structures[i].frac_coords)):
                    for k in range(3):
                        # update the current coordinates
                        current_wrapped_coords = xdatcar.structures[i].frac_coords[j][k]
                        displacement = unwrap_pbc_dis(
                            previous_unwrapped_coords[j][k], current_wrapped_coords, 1
                        )
                        current_unwrapped_coords[j][k] = (
                            previous_unwrapped_coords[j][k] + displacement
                        )

                # update the previous unwrapped coordinates for next frame
                previous_unwrapped_coords = current_unwrapped_coords.copy()

                # append the current structure's unwrapped coordinates to the list
                unwrapped_coords.append(current_unwrapped_coords)

            # open the output xyz file
            with open(output_path, "w") as xyz_file:
                for i, coords in enumerate(unwrapped_coords):
                    # write the current structure to the xyz file
                    xyz_file.write(str(len(xdatcar.structures[i].species)) + "\n\n")
                    for atom, coord in zip(xdatcar.structures[i].species, coords):
                        xyz_file.write(
                            "{} {:.8f} {:.8f} {:.8f}\n".format(atom.symbol, *coord)
                        )
            progress.update(task, advance=1)

    except Exception as e:
        console.log(e)
        console.log("🚌 xdatbus xdc_unwrap: Failed!")


def main():
    parser = argparse.ArgumentParser(
        description="Unwrap the coordinates in the XDATCAR file. The unwrapped coordinates will be written to a .xyz "
        "file."
    )
    parser.add_argument(
        "--xdc_path",
        type=str,
        default="./XDATBUS",
        help="Input path of the XDATCAR file",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="./XDATBUS_unwrap.xyz",
        help="Output path of the xyz file",
    )

    args = parser.parse_args()

    xdc_unwrap(args.xdc_path, args.output_path, show_progress=True)


if __name__ == "__main__":
    main()
