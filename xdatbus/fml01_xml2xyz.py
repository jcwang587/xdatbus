import os
import re
import argparse
from ase.io import read, write
from rich.console import Console
from rich.progress import Progress
from xdatbus.utils import filter_files


def xml2xyz(xml_dir="./", output_path="./", train_ratio=1.0):
    """
    Convert the vasprun.xml files to extended xyz files.

        Parameters
        ----------
        xml_dir : str
            Input path of the vasprun.xml files
        output_path : str
            Output path of the extended xyz files
        train_ratio : float (optional)
            The ratio of training set
    """

    console = Console(log_path=False)

    try:
        raw_list = os.listdir(xml_dir)
        xml_list = filter_files(raw_list, "vasprun")

        if len(xml_list) == 0:
            raise ValueError("No vasprun file found in the directory.")
        elif len(xml_list) == 1:
            xml_list_sort = xml_list
        else:
            xml_list_sort = sorted(
                xml_list, key=lambda x: int(re.findall(r"\d+", x)[0])
            )

        console.log(f"sequence: {xml_list_sort}")

        data_set = []
        with Progress(console=console) as progress:
            task = progress.add_task("🚌 xdatbus xml2xyz", total=len(xml_list_sort))
            for xml_file in xml_list_sort:
                progress.console.log(f"xml2xyz: processing {xml_file}")
                xml_path = os.path.join(xml_dir, xml_file)
                xml_set = read(xml_path, index="::", format="vasp-xml")
                for atom in xml_set:
                    if "free_energy" in atom.calc.results:
                        del atom.calc.results["free_energy"]
                data_set.extend(xml_set)
                progress.update(task, advance=1)

        if train_ratio < 1.0:
            train_set = data_set[: int(len(data_set) * train_ratio)]
            test_set = data_set[int(len(data_set) * train_ratio) :]
            write(os.path.join(output_path, "train.xyz"), train_set)
            write(os.path.join(output_path, "test.xyz"), test_set)
        else:
            write(os.path.join(output_path, "data.xyz"), data_set)

    except Exception as e:
        console.log(e)
        console.log("🚌 xdatbus xml2xyz: Failed!")


def main():
    parser = argparse.ArgumentParser(description="XML to XYZ converter")

    parser.add_argument(
        "--xml_dir",
        type=str,
        default="./",
        help="The directory containing the vasprun.xml files.",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        default="./",
        help="The directory to save the extended xyz files.",
    )

    parser.add_argument(
        "--train_ratio",
        type=float,
        default=1.0,
        help="The ratio of training set.",
    )

    args = parser.parse_args()

    xml2xyz(args.xml_dir, args.output_path, args.train_ratio)


if __name__ == "__main__":
    main()
