from rich.console import Console
from rich.table import Table


def main():
    console = Console()

    table = Table(title="XDATBUS HELP MENU", show_header=True, header_style="bold magenta")
    table.add_column("Command", style="dim", width=12)
    table.add_column("Description")

    # Add rows for each command
    table.add_row("xdc_aggregate", "Aggregate XDATCAR files from an AIMD simulation.")
    table.add_row("xdc_unwrap", "Unwrap the coordinates in the XDATCAR file (to .xyz format).")
    table.add_row("thermal_report", "Generate a thermal report from the OSZICAR files.")
    table.add_row("xml2xyz", "Convert the vasprun.xml files to extended xyz files.")

    console.print(table)


if __name__ == "__main__":
    main()
