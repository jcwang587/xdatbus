import os
import subprocess
import argparse


def bias(plumed_hills, plumed_outfile, plumed_mintozero, plumed_min, plumed_max):
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, './resources', 'sum_hills.sh')
    subprocess.run(['bash', str(script_path),
                    '--hills', str(plumed_hills),
                    '--outfile', str(plumed_outfile),
                    '--mintozero', str(plumed_mintozero),
                    '--min', str(plumed_min),
                    '--max', str(plumed_max)])


def main():
    parser = argparse.ArgumentParser(description="Apply sum_hills function from plumed that allows one to to use "
                                                 "plumed to post-process an existing hills/colvar file")
    parser.add_argument("--hills", type=str, default="HILLS",
                        help="Specify the name of the hills file (default: HILLS)")
    parser.add_argument("--outfile", type=str, default="./fes/fes_bias.dat",
                        help="specify the output file for sumhills (default: ./fes/fes_bias.dat)")
    parser.add_argument("--mintozero", type=str, default="on",
                        help="it translate all the minimum value in bias/histogram to zero (default: on)")
    parser.add_argument("--min", type=float, default=0.0,
                        help="the lower bounds for the grid (default: 0.0)")
    parser.add_argument("--max", type=float, default=1.0,
                        help="the upper bounds for the grid (default: 1.0)")
    parser.add_argument("--bin", type=int, default=100,
                        help="the number of bins for the grid (default: 100)")

    args = parser.parse_args()

    bias(args.hills, args.outfile, args.mintozero, args.min, args.max)


if __name__ == "__main__":
    main()
