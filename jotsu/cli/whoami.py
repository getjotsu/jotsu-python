import json

import click

from jotsu.cli import cli
from jotsu.client import Jotsu


@cli.command('whoami')
@click.option('--json', 'json_', is_flag=True)
def whoami(json_: bool):
    """ Display information about the user associated with the API Key. """
    with Jotsu() as client:
        res = client.get('/auth/me')
        res.raise_for_status()
        data = res.json()

        if json_:
            click.echo(json.dumps(data, indent=4))
        else:
            click.echo(data['email'])
