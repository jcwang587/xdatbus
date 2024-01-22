import pandas as pd
import plotly.express as px
from xdatbus.utils import skip_comments


def plot_fes():
    # load data from .dat file
    skip_lines = skip_comments('../tests/data/plumed/dat/fes_bias.dat')
    df = pd.read_csv('../tests/data/plumed/dat/fes_bias.dat', sep='\s+', header=None, skiprows=skip_lines)

    # plot with the first column to be x-axis, the second column to be y-axis
    fig = px.line(df, x=0, y=1)
    fig.show()




def main():
    plot_fes()


if __name__ == "__main__":
    main()
