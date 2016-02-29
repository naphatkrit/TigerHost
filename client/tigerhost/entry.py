import click

import tigerhost

from tigerhost.commands import apps, config, domains, git, keys
from tigerhost.commands.user import login, user_info, logout
from tigerhost.private_dir import ensure_private_dir_exists


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=tigerhost.__version__, prog_name='TigerHost')
def entry():
    ensure_private_dir_exists()

entry.add_command(login)
entry.add_command(logout)
entry.add_command(user_info, name='user:info')

entry.add_command(apps.list_apps, name='apps')
entry.add_command(apps.create_app, name='create')
entry.add_command(apps.destroy_app, name='apps:destroy')
entry.add_command(apps.transfer_app, name='apps:transfer')

entry.add_command(config.list_config, name='config')
entry.add_command(config.set_config, name='config:set')
entry.add_command(config.unset_config, name='config:unset')

entry.add_command(domains.list_domains, name='domains')
entry.add_command(domains.add_domain, name='domains:add')
entry.add_command(domains.remove_domain, name='domains:remove')

entry.add_command(git.add_remote, name='git:remote')

entry.add_command(keys.add_key, name='keys:add')
entry.add_command(keys.list_keys, name='keys')
entry.add_command(keys.remove_key, name='keys:remove')
