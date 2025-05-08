import os
import typing
from decimal import Decimal

import click


def calculate_total_cost(usage: typing.List[dict]) -> Decimal:
    total = Decimal(0)
    for entry in usage:
        cost = Decimal(entry.get('cost', 0))
        total += cost
    return total


def echo_usage(usage: typing.List[dict]):
    total = calculate_total_cost(usage)
    click.echo(f'Total cost: ${total}')
    for entry in usage:
        line = f"  {entry['model']}: ${entry['cost']}"
        if entry['input_tokens']:
            line += f", input_tokens={entry['input_tokens']}"
        if entry['output_tokens']:
            line += f", output_tokens={entry['output_tokens']}"
        click.echo(line)


def filename_without_extension(path: str) -> str:
    base_name = os.path.basename(path)
    name, _ = os.path.splitext(base_name)
    return name
