"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Phylm."""


if __name__ == "__main__":
    main(prog_name="phylm")  # pragma: no cover
