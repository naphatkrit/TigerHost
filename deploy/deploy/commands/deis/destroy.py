import boto3
import click

from click_extensions.decorators import print_markers

from deploy.secret import store
from deploy.utils.decorators import skip_if_debug


@click.command()
@click.option('--stack', '-s', default='deis', help='The name of the cloud formation stack to create.')
@print_markers
@skip_if_debug
def destroy(stack):
    """Destroy the deis cluster. This waits for the removal to complete.
    """
    cloudformation = boto3.resource('cloudformation')
    s = cloudformation.Stack(stack)
    stack_id = s.stack_id
    s.delete()
    click.echo('Delete initiated for stack {}.'.format(stack))
    click.echo('Waiting for deletion to complete.')
    client = boto3.client('cloudformation')
    waiter = client.get_waiter('stack_delete_complete')
    waiter.wait(StackName=stack_id)
    store.unset('deis__username')
    store.unset('deis__password')
    store.unset('deis__email')
