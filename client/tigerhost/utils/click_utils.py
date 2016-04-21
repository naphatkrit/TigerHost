import click


def echo_with_markers(text, marker='=', marker_color='blue'):
    """Print a text to the screen with markers surrounding it.

    The output looks like:
    ======== text ========
    with marker='=' right now.

    In the event that the terminal window is too small, the text is printed
    without markers.

    :param str text: the text to echo
    :param str marker: the marker to surround the text
    :param str marker_color: one of ('black' | 'red' | 'green' | 'yellow' | 'blue' | 'magenta' | 'cyan' | 'white')
    """
    text = ' ' + text + ' '
    width, _ = click.get_terminal_size()
    if len(text) >= width:
        click.echo(text)  # this is probably never the case
    else:
        leftovers = width - len(text)
        click.secho(marker * (leftovers / 2), fg=marker_color, nl=False)
        click.echo(text, nl=False)
        click.secho(marker * (leftovers / 2 + leftovers % 2), fg=marker_color)
