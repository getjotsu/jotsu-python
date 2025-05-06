import json

import click

from jotsu.cli import cli
from jotsu.client import Jotsu


@cli.command('whoami')
def whoami():
    """ Display information about the user associated with the API Key. """
    with Jotsu() as client:
        res = client.get('/auth/me')
        res.raise_for_status()
        click.echo(json.dumps(res.json(), indent=4))
