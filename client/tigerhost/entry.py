import click

from click_extensions import private_dir
from click_extensions.commands import bash_complete_command

import tigerhost

from tigerhost import settings
from tigerhost.commands import access, addons, apps, config, domains, git, keys, backends, run_command, logs
from tigerhost.commands.user import login, user_info, logout


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=tigerhost.__version__, prog_name='TigerHost')
def entry():
    private_dir.ensure_private_dir_exists(settings.APP_NAME)

entry.add_command(bash_complete_command(settings.APP_NAME))

entry.add_command(login)
entry.add_command(logout)
entry.add_command(user_info, name='user:info')

entry.add_command(apps.list_apps, name='apps')
entry.add_command(apps.create_app, name='create')
entry.add_command(apps.destroy_app, name='apps:destroy')
entry.add_command(apps.transfer_app, name='apps:transfer')

entry.add_command(access.get_users, name='access')
entry.add_command(access.add_access, name='access:add')
entry.add_command(access.remove_access, name='access:remove')

entry.add_command(addons.list_addons, name='addons')
entry.add_command(addons.create_addon, name='addons:create')
entry.add_command(addons.wait_addon, name='addons:wait')
entry.add_command(addons.delete_addon, name='addons:destroy')

entry.add_command(config.list_config, name='config')
entry.add_command(config.set_config, name='config:set')
entry.add_command(config.unset_config, name='config:unset')

entry.add_command(domains.list_domains, name='domains')
entry.add_command(domains.add_domain, name='domains:add')
entry.add_command(domains.remove_domain, name='domains:remove')

entry.add_command(logs.get_logs, name='logs')

entry.add_command(run_command.run_one_off, name='run')

entry.add_command(git.add_remote, name='git:remote')

entry.add_command(backends.list_backends, name='backends')

entry.add_command(keys.add_key, name='keys:add')
entry.add_command(keys.list_keys, name='keys')
entry.add_command(keys.remove_key, name='keys:remove')
