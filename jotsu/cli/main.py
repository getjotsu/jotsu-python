import click


@click.group()
@click.option('--json', 'json_', is_flag=True, default=False)
@click.pass_context
def cli(ctx, json_: bool):
    ctx.ensure_object(dict)
    ctx.obj['json'] = json_
