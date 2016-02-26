import click

from functools import update_wrapper

from tigerhost import exit_codes, settings
from tigerhost.api_client import ApiClient, ApiClientAuthenticationError
from tigerhost.user import load_user, has_saved_user
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


def catch_exception(exception, message=None):
    def decorator(f):
        @click.pass_context
        def new_func(ctx, *args, **kwargs):
            try:
                return ctx.invoke(f, *args, **kwargs)
            except exception as e:
                message1 = message if message is not None else '{}'.format(e)
                click.echo(message1)
                ctx.exit(code=exit_codes.OTHER_FAILURE)
        return update_wrapper(new_func, f)
    return decorator


def pass_user(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        if not has_saved_user():
            click.echo('Not logged in. Please run `tigerhost login`.')
            ctx.exit(code=exit_codes.OTHER_FAILURE)
        else:
            user = load_user()
            client = ApiClient(
                api_server_url=settings.API_SERVER_URL,
                username=user.username,
                api_key=user.api_key,
            )
            try:
                client.test_api_key()
            except ApiClientAuthenticationError:
                click.echo(
                    'Credentials no longer valid. Please run `tigerhost login` again.')
                ctx.exit(code=exit_codes.OTHER_FAILURE)
            return ctx.invoke(f, user, *args, **kwargs)
    return update_wrapper(new_func, f)


def pass_api_client(f):
    @pass_user
    @click.pass_context
    def new_func(ctx, user, *args, **kwargs):
        client = ApiClient(
            api_server_url=settings.API_SERVER_URL,
            username=user.username,
            api_key=user.api_key,
        )
        return ctx.invoke(f, client, *args, **kwargs)
    return update_wrapper(new_func, f)
