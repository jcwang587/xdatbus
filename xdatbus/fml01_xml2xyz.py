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

        print("xdatbus-func | xml2xyz: Done!")

    except Exception as e:
        print(e)
        print("xdatbus-func | xml2xyz: Failed!")
