import csv
import errno
import json
import sys

import click

from jotsu.cli import cli
from jotsu.client import Jotsu
from .utils import echo_usage, filename_without_extension


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


def _document_create(corpus_id: str, json_data: dict, *, verbose: bool, json_: bool):
    with Jotsu() as client:
        res = client.post(f'/services/rag/corpora/{corpus_id}/documents', json=json_data)
        res.raise_for_status()

        doc = res.json()
        if json_:
            click.echo(json.dumps(doc))
        else:
            click.echo(f"[{doc['id']}] {doc['name']}")
            if verbose:
                click.echo()
                echo_usage(doc['usage'])
                click.echo()


@documents.command('create')
@click.option('--corpus-id', required=True)
@click.option('--name', required=True)
@click.option('--text', required=True)
@click.option('--path', default='/')
@click.option('--json', 'json_', is_flag=True)
@click.option('--verbose', '-v', is_flag=True)
def documents_create(corpus_id: str, json_: bool, verbose: bool, **kwargs):
    return _document_create(corpus_id, kwargs, json_=json_, verbose=verbose)


@documents.command('load')
@click.argument('filepath')
@click.option('--corpus-id', required=True)
@click.option('--name', default=None)
@click.option('--path', default='/')
@click.option('--json', 'json_', is_flag=True)
@click.option('--verbose', '-v', is_flag=True)
def documents_load(filepath: str, corpus_id: str, json_: bool, verbose: bool, name: str, path: str):
    with open(filepath, 'r') as f:
        text = f.read()

    json_data = {
        'name': name if name else filename_without_extension(filepath),
        'path': path,
        'text': text
    }

    return _document_create(corpus_id, json_data, json_=json_, verbose=verbose)


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


@documents.command('csv')
@click.argument('path')
@click.option('--name-column', prompt=True)
@click.option('--text-column', prompt=True)
@click.option('--corpus-id', prompt=True)
@click.option('--delimiter', default=',')
@click.option('--json', 'json_', is_flag=True)
def docs_csv(path: str, corpus_id: str, name_column: str, text_column: str, delimiter: str, json_: bool):
    results = []
    with Jotsu() as client:
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                json_data = {
                    'name': row[name_column],
                    'text': row[text_column]
                }

                res = client.post(f'/services/rag/corpora/{corpus_id}/documents', json=json_data)
                res.raise_for_status()
                results.append(res.json())


    if json_:
        for doc in results:
            click.echo(json.dumps(doc))
    else:
        click.echo(f'OK: {len(results)} documents.')
