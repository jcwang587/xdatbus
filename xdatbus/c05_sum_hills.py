import os
import subprocess
import argparse


def sum_hills(
    plumed_hills, plumed_outfile, plumed_min, plumed_max, plumed_bin, plumed_eachstep
):
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, "resources", "sum_hills.sh")

    if plumed_eachstep:
        pass
    else:
        subprocess.run(
            [
                "bash",
                script_path,
                "--hills",
                str(plumed_hills),
                "--outfile",
                str(plumed_outfile),
                "--min",
                str(plumed_min),
                "--max",
                str(plumed_max),
                "--bin",
                str(plumed_bin),
            ]
        )


def main():
    parser = argparse.ArgumentParser(
        description="Apply sum_hills function from plumed that allows one to to use "
        "plumed to post-process an existing hills/colvar file"
    )
    parser.add_argument(
        "--hills",
        type=str,
        default="HILLS",
        help="specify the name of the hills file (default: HILLS)",
    )
    parser.add_argument(
        "--outfile",
        type=str,
        default="fes_bias.dat",
        help="specify the output file for sumhills (default: fes_bias.dat)",
    )
    parser.add_argument(
        "--min",
        type=float,
        default=0.0,
        help="the lower bounds for the grid (default: 0.0)",
    )
    parser.add_argument(
        "--max",
        type=float,
        default=1.0,
        help="the upper bounds for the grid (default: 1.0)",
    )
    parser.add_argument(
        "--bin",
        type=int,
        default=100,
        help="the number of bins for the grid (default: 100)",
    )
    parser.add_argument(
        "--eachstep",
        type=bool,
        default=False,
        help="if true, the output will be written into a separate json file for each step",
    )

    args = parser.parse_args()

    sum_hills(args.hills, args.outfile, args.min, args.max, args.bin, args.eachstep)


if __name__ == "__main__":
    main()
