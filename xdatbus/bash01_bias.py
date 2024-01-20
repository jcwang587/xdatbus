import os
import subprocess
import argparse


def bias():
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, './resources', 'sum_hills.sh')
    subprocess.run(['bash', script_path])


def main():
    parser = argparse.ArgumentParser(description="Aggregate XDATCAR files from an AIMD simulation.")
    parser.add_argument("--xdc_dir", type=str,
                        help="Input path of the AIMD simulation, which contains the XDATCAR files")
    parser.add_argument("--output_path", type=str, default="./",
                        help="Output path of the XDATBUS file (default: current directory)")
    parser.add_argument("--delete_temp_files", action="store_true",
                        help="If set, the intermediate folders will be deleted (default: False)")

    args = parser.parse_args()

    bias()


if __name__ == "__main__":
    main()
