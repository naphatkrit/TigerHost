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


def _bash_complete_name(app_name):
    """Given the name of the app, create the equivalent bash-complete
    name. This is the uppercase version of the app name with dashes
    replaced by underscores.

    :param str app_name: the name of the app

    :rtype: str
    :returns: app_name uppercased, with dashes replaced by underscores.
    """
    return app_name.upper().replace('-', '_')


def bash_complete_command(app_name):
    """Return a command that outputs the script that the user can run
    to activate bash completion.

    :param str app_name: the name of the app
    """
    @click.command('bash-complete')
    @click.pass_context
    def bash_complete(ctx):
        """Display the commands to set up bash completion.
        """
        bash_name = _bash_complete_name(app_name)
        click.echo("""
eval "`_{bash_name}_COMPLETE=source {app_name}`"
# Run this command to configure your shell:
# eval `{command}`
""".format(
            bash_name=bash_name,
            app_name=app_name,
            command=ctx.command_path
        ).strip())
    return bash_complete
