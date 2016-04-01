import click


def echo_with_markers(text, marker='='):
    text = ' ' + text + ' '
    width, _ = click.get_terminal_size()
    if len(text) >= width:
        click.echo(text)  # this is probably never the case
    else:
        leftovers = width - len(text)
        click.echo(marker * (leftovers / 2), nl=False)
        click.echo(text, nl=False)
        click.echo(marker * (leftovers / 2 + leftovers % 2))


def full_command_name(ctx):
    """Get the full executed command name. For example,

    tigerhost create

    @type ctx: click.Context

    @rtype: str
    """
    name = []
    while ctx is not None:
        name.append(ctx.info_name)
        ctx = ctx.parent
    return ' '.join(reversed(name))
