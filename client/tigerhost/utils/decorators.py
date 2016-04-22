import click
import urlparse

from functools import update_wrapper

from tigerhost import exit_codes, settings
from tigerhost.api_client import ApiClient, ApiClientAuthenticationError
from tigerhost.user import load_user, has_saved_user
from tigerhost.utils import click_utils
from tigerhost.vcs.base import CommandError
from tigerhost.vcs.git import GitVcs


def print_markers(f):
    """A decorator that prints the invoked command
    before and after the command.
    """
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        command = ctx.info_name
        assert command is not None
        command_name = ctx.command_path
        click_utils.echo_with_markers(command_name, marker_color='green')

        def print_error(code):
            click_utils.echo_with_markers('end of {} (exit code: {code})'.format(
                command_name, code=code), marker_color='red')
        try:
            ctx.invoke(f, *args, **kwargs)
        except SystemExit as e:
            code = e.code if e.code is not None else exit_codes.ABORT
            print_error(code)
            raise
        except click.ClickException as e:
            code = e.exit_code
            print_error(code)
            raise
        except click.Abort as e:
            code = exit_codes.ABORT
            print_error(code)
            raise
        except Exception as e:
            code = -1
            print_error(code)
            raise
        else:
            click_utils.echo_with_markers('end of {}'.format(
                command_name), marker_color='green')
            return
    return update_wrapper(new_func, f)


def ensure_obj(f):
    """A decorator that ensures context.obj exists
    """
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        if ctx.obj is None:
            ctx.obj = {}
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def store_vcs(f):
    """A decorator that store the VCS object into
    the object.
    """
    # TODO ideally we should detect the type of VCS.
    # But for now, we only support git
    @click.pass_context
    @ensure_obj
    def new_func(ctx, *args, **kwargs):
        if 'vcs' in ctx.obj:
            return ctx.invoke(f, *args, **kwargs)
        # if not a repository, pass ``None``
        try:
            vcs = GitVcs()
        except CommandError:
            vcs = None
        ctx.obj['vcs'] = vcs
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def catch_exception(exception, message=None):
    """A decorator that gracefully handles exceptions, exiting
    with :py:obj:`exit_codes.OTHER_FAILURE`.
    """
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


def store_user(f):
    """A decorator that store the user object in context.obj.

    If the user does not exist, then exit with an error message
    """
    @click.pass_context
    @ensure_obj
    def new_func(ctx, *args, **kwargs):
        if 'user' in ctx.obj:
            return ctx.invoke(f, *args, **kwargs)
        if not has_saved_user():
            click.echo('Not logged in. Please run `{app_name} login`.'.format(
                app_name=settings.APP_NAME))
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
                    'Credentials no longer valid. Please run `{app_name} login` again.'.format(app_name=settings.APP_NAME))
                ctx.exit(code=exit_codes.OTHER_FAILURE)
            ctx.obj['user'] = user
            return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def store_api_client(f):
    """A decorator that stores the API client in context.obj
    """
    @store_user
    @click.pass_context
    @ensure_obj
    def new_func(ctx, *args, **kwargs):
        if 'api_client' in ctx.obj:
            return ctx.invoke(f, *args, **kwargs)
        user = ctx.obj['user']
        client = ApiClient(
            api_server_url=settings.API_SERVER_URL,
            username=user.username,
            api_key=user.api_key,
        )
        ctx.obj['api_client'] = client
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


def store_app(f):
    """A decorator that stores the app name in context.obj

    The app name comes from git remote tigerhost, and can be
    overidden with the option --app/-a.
    """
    @click.option('--app', '-a', help='The app to work with')
    @store_vcs
    @click.pass_context
    @ensure_obj
    def new_func(ctx, app, *args, **kwargs):
        if 'app' in ctx.obj:
            return ctx.invoke(f, *args, **kwargs)
        vcs = ctx.obj['vcs']
        if app is not None:
            ctx.obj['app'] = app
            return ctx.invoke(f, *args, **kwargs)
        if vcs is None:
            click.echo(
                'Not in a git repository. Could not determine a default app. Please rerun with `--app APP`.')
            ctx.exit(code=exit_codes.OTHER_FAILURE)
        remotes = vcs.get_remotes()
        if settings.APP_NAME not in remotes:
            click.echo(
                'No git remote {app_name}. Could not determine a default app. Please rerun with `--app APP`.'.format(app_name=settings.APP_NAME))
            ctx.exit(code=exit_codes.OTHER_FAILURE)
        parsed = urlparse.urlparse(remotes[settings.APP_NAME])
        app = parsed.path.strip('/').split('.')[0]
        ctx.obj['app'] = app
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)
