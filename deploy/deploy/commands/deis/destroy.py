import boto3
import click

from tigerhost.utils.decorators import print_markers

from deploy import settings


@click.command()
@click.option('--stack', '-s', default='deis', help='The name of the cloud formation stack to create.')
@print_markers
def destroy(stack):
    if settings.DEBUG:
        click.echo('Not doing anything because DEBUG is True.')
        return
    cloudformation = boto3.resource('cloudformation')
    s = cloudformation.Stack(stack)
    stack_id = s.stack_id
    s.delete()
    click.echo('Delete initiated for stack {}.'.format(stack))
    click.echo('Waiting for deletion to complete.')
    client = boto3.client('cloudformation')
    waiter = client.get_waiter('stack_delete_complete')
    waiter.wait(StackName=stack_id)
