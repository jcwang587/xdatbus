import pandas as pd
from .utils import skip_comments


def plotfes():
    # load data from .dat file
    skip_lines = skip_comments('../tests/data/plumed/dat/fes_bias.dat')
    df = pd.read_csv('../tests/data/plumed/dat/fes_bias.dat', sep='\s+', header=None, skiprows=skip_lines)


def main():
    plotfes()


if __name__ == "__main__":
    main()
