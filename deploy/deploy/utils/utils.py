import boto3
import random
import string


def random_string(length, allowed_chars=string.ascii_letters + string.digits):
    rand = random.SystemRandom()
    return ''.join(rand.choice(allowed_chars) for _ in range(length))


def parse_shell_for_exports(text):
    """Parses a shell script and extracts all of its exports.

    @type text: str
        The shell script

    @rtype: dict
        for example,

        export VAR1=value1
        ...
        export VAR2="value2"

        will return:

        {
            'VAR1': 'value1',
            'VAR2': 'value2',
        }
    """
    lines = [x for x in text.split('\n') if x.startswith('export ')]
    lines = [x[len('export '):] for x in lines]
    env = dict()
    for l in lines:
        key, value = l.split('=', 1)
        value = value.split('#', 1)[0].strip().strip('"').strip("'")
        env[key] = value
    return env


def set_aws_security_group_ingress_rule(group_name, fromPort, toPort, cidrIp):
    """Add an ingress rule to a security group.

    @type group_name: str
    @type fromPort: int
    @type toPort: int
    @type cidrIp: str
    """
    ec2 = boto3.resource('ec2')
    group = list(ec2.security_groups.filter(GroupNames=[group_name]).limit(1))[0]
    found = False
    for perm in group.ip_permissions:
        if perm['FromPort'] != fromPort or perm['ToPort'] != toPort or perm['IpProtocol'] != 'tcp':
            continue
        for ip in perm['IpRanges']:
            if ip['CidrIp'] == cidrIp:
                found = True
    if not found:
        group.authorize_ingress(IpProtocol='tcp', FromPort=0, ToPort=65535, CidrIp='0.0.0.0/0')
