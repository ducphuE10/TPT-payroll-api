import logging

import click

log = logging.getLogger(__name__)


@click.group()
def payroll_cli():
    """Command-line interface to Payroll."""
    from .logging import configure_logging

    configure_logging()


@payroll_cli.group("database")
def payroll_database():
    """Container for all payroll database commands."""
    pass


@payroll_database.command("init")
def database_init():
    """Initializes a new database."""
    click.echo("Initializing new database...")
    from .database.core import engine
    from .database.manage import init_database

    init_database(engine)
    click.secho("Success.", fg="green")


def entrypoint():
    """The entry that the CLI is executed from"""
    from .exceptions import PayrollException

    try:
        payroll_cli()
    except PayrollException as e:
        click.secho(f"ERROR: {e}", bold=True, fg="red")


if __name__ == "__main__":
    entrypoint()
