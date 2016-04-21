import click


def echo_with_markers(text, marker='=', marker_color='blue', text_color=None):
    """Print a text to the screen with markers surrounding it.

    The output looks like:
    ======== text ========
    with marker='=' right now.

    In the event that the terminal window is too small, the text is printed
    without markers.

    :param str text: the text to echo
    :param str marker: the marker to surround the text
    :param str marker_color: one of ('black' | 'red' | 'green' | 'yellow' | 'blue' | 'magenta' | 'cyan' | 'white')
    :param str text_color: one of ('black' | 'red' | 'green' | 'yellow' | 'blue' | 'magenta' | 'cyan' | 'white')
    """
    text = ' ' + text + ' '
    width, _ = click.get_terminal_size()
    if len(text) >= width:
        click.echo(text)  # this is probably never the case
    else:
        leftovers = width - len(text)
        click.secho(marker * (leftovers / 2), fg=marker_color, nl=False)
        click.secho(text, nl=False, fg=text_color)
        click.secho(marker * (leftovers / 2 + leftovers % 2), fg=marker_color)


def echo_heading(text, marker='=', marker_color='blue'):
    """Print a text formatted to look like a heading.

    The output looks like:
    ===> text
    with marker='=' right now.

    :param str text: the text to echo
    :param str marker: the marker to mark the heading
    :param str marker_color: one of ('black' | 'red' | 'green' | 'yellow' | 'blue' | 'magenta' | 'cyan' | 'white')
    """
    click.secho(marker * 3 + '>', fg=marker_color, nl=False)
    click.echo(' ' + text)
