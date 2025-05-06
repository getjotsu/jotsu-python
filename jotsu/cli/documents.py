import errno
import json
import sys

import click

from jotsu.cli import cli
from jotsu.client import Jotsu


@cli.group('documents')
def documents():
    """ Individual documents in a corpus. """
    pass


@documents.command('list')
@click.option('--corpus-id', prompt=True)
@click.option('--json', 'json_', is_flag=True)
def documents_list(corpus_id: str, json_: bool):
    with Jotsu() as client:
        res = client.get(f'/services/rag/corpora/{corpus_id}/documents?order_by=name')
        res.raise_for_status()
        data = res.json()

        if data['total'] == 0:
            if not json_:
                click.echo('That corpus is empty.')
            sys.exit(errno.ENOENT)

        for corpus in res.json()['data']:
            if json_:
                click.echo(json.dumps(corpus))
            else:
                click.echo(f"[{corpus['id']}] {corpus['name']}")


@documents.command('create')
@click.option('--corpus-id', required=True)
@click.option('--name', required=True)
@click.option('--text', required=True)
@click.option('--path', default='/')
@click.option('--json', 'json_', is_flag=True)
def documents_create(corpus_id: str, json_: bool, **kwargs):

    with Jotsu() as client:
        res = client.post(f'/services/rag/corpora/{corpus_id}/documents', json=kwargs)
        res.raise_for_status()

        doc = res.json()
        if json_:
            click.echo(json.dumps(doc))
        else:
            click.echo(f"[{doc['id']}] {doc['name']}")


@documents.command('delete')
@click.argument('document_id')
@click.option('--json', 'json_', is_flag=True)
@click.option('--force', '-f', is_flag=True)
def documents_delete(document_id: str, json_: bool, force: bool):
    if not force:
        if not click.confirm('Do you want to PERMANENTLY delete this document?'):
            return

    with Jotsu() as client:
        res = client.delete(f'/services/rag/documents/{document_id}')
        res.raise_for_status()

        doc = res.json()
        if json_:
            click.echo(json.dumps(doc))
        else:
            click.echo(f"Document {doc['id']} deleted successfully.")
