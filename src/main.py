"""Package entrypoint so that `python -m src` runs the CLI."""

from . import cli

if __name__ == '__main__':
    cli.main()
