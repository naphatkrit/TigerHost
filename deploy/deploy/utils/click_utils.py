import click


def prompt_choices(choices):
    """Displays a prompt for the given choices

    :param list choices: the choices for the user to choose from

    :rtype: int
    :returns: the index of the chosen choice
    """
    assert len(choices) > 1
    for i in range(len(choices)):
        click.echo('{number}) {choice}'.format(
            number=i + 1,
            choice=choices[i]
        ))
    value = click.prompt('1-{}'.format(len(choices)), type=int) - 1
    if value < 0 or value >= len(choices):
        raise click.ClickException('Invalid choice.')
    return value
