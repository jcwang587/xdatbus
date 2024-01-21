import os
import subprocess
import argparse


def bias(plumed_min, plumed_max, plumed_bin):
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, 'resources', 'sum_hills.sh')
    subprocess.run(['bash', script_path,
                    '--min', str(plumed_min),
                    '--max', str(plumed_max),
                    '--bin', str(plumed_bin)])


def main():
    parser = argparse.ArgumentParser(description="Apply sum_hills function from plumed that allows one to to use "
                                                 "plumed to post-process an existing hills/colvar file")
    parser.add_argument("--min", type=float, default=0.0,
                        help="the lower bounds for the grid (default: 0.0)")
    parser.add_argument("--max", type=float, default=1.0,
                        help="the upper bounds for the grid (default: 1.0)")
    parser.add_argument("--bin", type=int, default=100,
                        help="the number of bins for the grid (default: 100)")

    args = parser.parse_args()

    bias(args.min, args.max, args.bin)


if __name__ == "__main__":
    main()
