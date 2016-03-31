import click


def echo_with_markers(text, marker='='):
    width, _ = click.get_terminal_size()
    if len(text) >= width:
        click.echo(text)  # this is probably never the case
    else:
        leftovers = width - len(text)
        click.echo(marker * (leftovers / 2), nl=False)
        click.echo(text, nl=False)
        click.echo(marker * (leftovers / 2 + leftovers % 2))
