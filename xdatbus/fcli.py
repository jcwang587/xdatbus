from rich.console import Console
from rich.table import Table


def main():
    console = Console()

    table = Table(
        title="XDATBUS CLI RECIPES", title_style="bold magenta"
    )
    table.add_column("CLI Command", style="cyan")
    table.add_column("Options")
    table.add_column("Description")

    # Add rows for each command
    table.add_row(
        "xdc_aggregate",
        "[--xdc_dir] [--output_dir] [--del_temp]",
        "Aggregate XDATCAR files from an AIMD simulation",
    )
    table.add_row(
        "xdc_unwrap",
        "[--xdc_path] [--output_path]",
        "Unwrap the coordinates in the XDATCAR file (to xyz)",
    )
    table.add_row(
        "thermal_report",
        "[--osz_dir] [--output_path]",
        "Generate a thermal report from the OSZICAR files",
    )
    table.add_row(
        "xml2xyz",
        "[--xml_dir] [--output_path] [--train_ratio]",
        "Convert the vasprun.xml files to extended xyz files",
    )

    console.print(table)


if __name__ == "__main__":
    main()
