import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

@click.group()
def instances():
    """Comands for instances"""

@instances.command("list")
@click.option("--project", default=None,
    help = "only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    instances = []

    if project:
        filters = [{"Name":"tag:Project", "Values":[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        print(', '.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name)))

    return

@instances.command("stop")
@click.option("--project", default=None,
    help="Only instaces for project")
def stop_instances(project):
    "stop Ec2 instances"

    instances = []

    if project:
        filters = [{"Name":"tag:Project", "Values":[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        print("Stopping {0}...". format(i.id))
        i.stop()

    return

if __name__ == '__main__':
    instances()
