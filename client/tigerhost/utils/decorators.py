import click

from functools import update_wrapper

from tigerhost.vcs.git import GitVcs


def print_markers(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        command = ctx.info_name
        assert command is not None
        _print_marker(' tigerhost ' + command + ' ')
        try:
            return ctx.invoke(f, *args, **kwargs)
        finally:
            _print_marker(' end of tigerhost ' + command + ' ')
    return update_wrapper(new_func, f)


def _print_marker(text):
    width, _ = click.get_terminal_size()
    if len(text) >= width:
        click.echo(text)  # this is probably never the case
    else:
        leftovers = width - len(text)
        click.echo('=' * (leftovers / 2), nl=False)
        click.echo(text, nl=False)
        click.echo('=' * (leftovers / 2 + leftovers % 2))


def pass_vcs(f):
    # TODO ideally we should detect the type of VCS.
    # But for now, we only support git
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        vcs = GitVcs()
        return ctx.invoke(f, vcs, *args, **kwargs)
    return update_wrapper(new_func, f)


def catch_exception(exception):
    def decorator(f):
        @click.pass_context
        def new_func(ctx, *args, **kwargs):
            try:
                return ctx.invoke(f, *args, **kwargs)
            except exception as e:
                ctx.fail('Exceptoin: {}'.format(e))
        return update_wrapper(new_func, f)
    return decorator
