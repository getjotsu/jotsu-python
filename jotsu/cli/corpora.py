import errno
import json
import sys

import click

from jotsu.cli import cli
from jotsu.client import Jotsu


@cli.group('corpora')
def corpora():
    """ Collections of documents """
    pass


@corpora.command('list')
@click.option('--json', 'json_', is_flag=True)
def corpora_list(json_: bool):
    with Jotsu() as client:
        res = client.get('/services/rag/corpora?order_by=name')
        res.raise_for_status()
        data = res.json()

        if data['total'] == 0:
            if not json_:
                click.echo('No corpora found.')
            sys.exit(errno.ENOENT)

        for corpus in res.json()['data']:
            if json_:
                click.echo(json.dumps(corpus))
            else:
                click.echo(f"[{corpus['id']}] {corpus['name']}")


@corpora.command('create')
@click.argument('name')
@click.option('--description', default=None)
@click.option('--media-type', type=click.Choice(['text/plain', 'text/markdown']), default='text/plain')
@click.option('--chunk-size', type=click.IntRange(1), default=1000)
@click.option('--chunk-overlap', type=click.IntRange(0), default=200)
@click.option('--json', 'json_', is_flag=True)
def corpora_create(**kwargs):
    json_ = kwargs.pop('json_', False)

    with Jotsu() as client:
        res = client.post('/services/rag/corpora', json=kwargs)
        res.raise_for_status()

        corpus = res.json()
        if json_:
            click.echo(json.dumps(corpus))
        else:
            click.echo(f"[{corpus['id']}] {corpus['name']}")


@corpora.command('delete')
@click.argument('corpus_id')
@click.option('--json', 'json_', is_flag=True)
@click.option('--force', '-f', is_flag=True)
def corpora_delete(corpus_id: str, json_: bool, force: bool):
    if not force:
        if not click.confirm('Do you want to PERMANENTLY delete this corpus and all documents it contains?'):
            return

    with Jotsu() as client:
        res = client.delete(f'/services/rag/corpora/{corpus_id}')
        res.raise_for_status()

        corpus = res.json()
        if json_:
            click.echo(json.dumps(corpus))
        else:
            click.echo(f"Corpus {corpus['id']} deleted successfully.")
