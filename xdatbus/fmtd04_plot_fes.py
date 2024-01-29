import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import argparse
from xdatbus.utils import skip_comments
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_fes(dat_file="fes_bias.dat", hills_file="HILLS"):
    # Load data from .dat file
    dat = pd.read_csv(
        dat_file, sep="\s+", header=None, skiprows=skip_comments(dat_file)
    )
    hills = pd.read_csv(
        hills_file, sep="\s+", header=None, skiprows=skip_comments(hills_file)
    )

    fig = make_subplots(rows=1, cols=2, subplot_titles=("CV Plot", "FES Plot"))

    fig.add_trace(
        go.Scatter(x=hills[0], y=hills[1], mode="lines", name="CV"), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=dat[0], y=dat[1], mode="lines", name="FES"), row=1, col=2
    )

    # Make layout responsive
    fig.update_layout(
        autosize=True,
        margin=dict(l=25, r=25, t=25, b=25),
    )
    return fig


def dash_app(dat_file="fes_bias.dat", hills_file="HILLS"):
    # Initialize the Dash app
    app = dash.Dash(__name__)

    # App layout
    app.layout = html.Div(
        [
            dcc.Graph(id="main-plot", figure=plot_fes(dat_file, hills_file)),
            html.Div(id="hover-data"),
        ]
    )

    @app.callback(
        Output("main-plot", "figure"),
        [Input("main-plot", "hoverData")],
        [State("main-plot", "figure")],
    )
    def update_fes_plot(hover_data, fig):
        # Check if hoverData is available and if the hover is on the first trace (CV plot)
        if (
            hover_data
            and hover_data["points"]
            and hover_data["points"][0]["curveNumber"] == 0
        ):
            y_value = hover_data["points"][0]["y"]

            # Calculate the width of the rectangle as 1/100th of the x-axis range
            x_range = fig["layout"]["xaxis2"]["range"]
            rect_width = (x_range[1] - x_range[0]) / 100

            # Define the vertical rectangle shape
            new_shape = dict(
                type="rect",
                xref="x2",
                yref="paper",
                x0=y_value - rect_width / 2,
                y0=0,
                x1=y_value + rect_width / 2,
                y1=1,
                fillcolor="LightSkyBlue",
                opacity=0.5,
                line_width=0,
            )
            # Update or add the new shape
            fig["layout"]["shapes"] = [new_shape]

        else:
            # Remove the line when not hovering over the CV plot
            fig["layout"]["shapes"] = []

        return fig

    app.run_server(debug=False, host="0.0.0.0", port=8000)


def main():
    parser = argparse.ArgumentParser(
        description="Plot the free energy surface from plumed output file"
    )
    parser.add_argument(
        "--dat",
        type=str,
        default="fes_bias.dat",
        help="specify the name of the dat file (default: fes_bias.dat)",
    )
    parser.add_argument(
        "--hills",
        type=str,
        default="HILLS",
        help="specify the name of the hills file (default: HILLS)",
    )
    parser.add_argument(
        "--dash",
        type=bool,
        default=False,
        help="specify whether to use dash (default: False)",
    )

    args = parser.parse_args()

    if args.dash:
        dash_app(args.dat, args.hills)
    else:
        fig = plot_fes(args.dat, args.hills)
        fig.write_image("fes.png")


if __name__ == "__main__":
    main()
