from rich.console import Console
from rich.table import Table


def main():
    console = Console()

    table = Table(title="XDATBUS HELP MENU", show_header=True, header_style="bold magenta")
    table.add_column("Command", style="dim", width=12)
    table.add_column("Description")

    # Add rows for each command
    table.add_row("command1", "Description of command1")
    table.add_row("command2", "Description of command2")

    console.print(table)


if __name__ == "__main__":
    main()
