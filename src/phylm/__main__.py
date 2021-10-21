"""Command-line interface."""
import click


# @click.version_option results in "untyped decorator" error
# https://github.com/python/typeshed/issues/5642


@click.command()
@click.version_option()  # type: ignore[misc]
def main() -> None:
    """Phylm."""


if __name__ == "__main__":
    main(prog_name="phylm")  # pragma: no cover
