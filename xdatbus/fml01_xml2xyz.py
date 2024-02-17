import os
import re
import argparse
from ase.io import read, write
from xdatbus.utils import filter_files

# load the vasprun.xml file
train_set = read("run1/vasprun.xml", index="::")
test_set = read("run2/vasprun.xml", index="::")

# write the atoms object to extended xyz file with forces
write("train.xyz", train_set)
write("test.xyz", test_set)


def xml2xyz(xml_dir="./", output_path="./"):
    try:
        raw_list = os.listdir(xml_dir)
        xml_list = filter_files(raw_list, "vasprun.xml")

        if len(xml_list) == 0:
            raise ValueError("No vasprun.xml file found in the directory.")

        xml_list_sort = sorted(xml_list, key=lambda x: int(re.findall(r"\d+", x)[0]))

        for xml_file in xml_list_sort:
            print(f"xdatbus-func | xml2xyz: Processing {xml_file}")
            xml_path = os.path.join(xml_dir, xml_file)
            xml_set = read(xml_path, index="::")
            xyz_path = os.path.join(output_path, f"{xml_file}.xyz")
            write(xyz_path, xml_set)

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

    )

    args = parser.parse_args()

    xml2xyz(args.xml_dir, args.output_path)


if __name__ == "__main__":
    main()
