import sys

import click

from jotsu.cli import cli


@cli.command('whoami')
def whoami():
    """ Display information about the user associated with the API Key. """
