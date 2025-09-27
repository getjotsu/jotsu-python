import errno
import json
import sys

import click

from jotsu.cli import cli
from jotsu.client import Jotsu


@cli.group('workflows')
def workflows():
    """ Automations """
    pass


@workflows.command('list')
@click.pass_context
def workflows_list(ctx):

    with Jotsu() as client:
        res = client.get('/workflows?order_by=name')
        res.raise_for_status()
        data = res.json()

        if data['total'] == 0:
            if not ctx.obj['json']:
                click.echo('No workflows found.')
            sys.exit(errno.ENOENT)

        for workflow in res.json()['data']:
            if ctx.obj['json']:
                click.echo(json.dumps(workflow))
            else:
                line = f'[{workflow["id"]}] {workflow["name"]}'
                if workflow.get('description'):
                    line += ' - ' + workflow.get('description')
                print(line)


@workflows.command('run')
@click.argument('workflow_id')
def workflow_run(workflow_id: str):
    with Jotsu() as client:
        with client.stream('POST', f'/workflows/{workflow_id}/run', json={'data': None}, timeout=60) as res:
            res.raise_for_status()
            for line in res.iter_lines():
                if line:
                    print(line)
