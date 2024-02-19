import os
import re
import argparse
from ase.io import read, write
from xdatbus.utils import filter_files


def xml2xyz(xml_dir="./", output_path="./", train_ratio=1.0):
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

        data_set = []
        for xml_file in xml_list_sort:
            print(f"xdatbus-func | xml2xyz: Processing {xml_file}")
            xml_path = os.path.join(xml_dir, xml_file)
            xml_set = read(xml_path, index="::", format="vasp-xml")
            for atom in xml_set:
                if "free_energy" in atom.calc.results:
                    del atom.calc.results["free_energy"]
            data_set.extend(xml_set)

        if train_ratio < 1.0:
            train_set = data_set[: int(len(data_set) * train_ratio)]
            test_set = data_set[int(len(data_set) * train_ratio) :]
            write(os.path.join(output_path, "train.xyz"), train_set)
            write(os.path.join(output_path, "test.xyz"), test_set)
        else:
            write(os.path.join(output_path, "data.xyz"), data_set)

        print("sequence: ", xml_list_sort)
        print("xdatbus-func | xml2xyz: Done!")

    except Exception as e:
        print(e)
        print("xdatbus-func | xml2xyz: Failed!")


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
