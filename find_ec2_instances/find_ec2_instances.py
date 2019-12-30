import boto3
import click

session = boto3.Session(profile_name='personal')
ec2 = session.resource('ec2')

def filter_instances(project):
    if project:
        filters = [{'Name': 'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """Managing snapshots"""

@cli.group()
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, help="Only volumes for project(tag Project:<name>)")
def list_volumes(project):
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
                v.id,
                i.id,
                v.state,
                str(v.size) + 'GiB',
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

@cli.group()
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, help="Only volumes for project(tag Project:<name>)")
def list_snapshots(project):
    "List volume snapshots"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime('%c')
                )))
    return


@cli.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List ec2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key'] : t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>'))))

    return

@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Starting {0}".format(i.id))
        i.start()

    return

@instances.command('snapshot')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def create_snapshot(project):
    "Create snapshot of instance"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print('Creating Snapshot of {0}'.format(i.id))
            v.create_snapshot(Description='Created by snapshotanalyzer')

    return




if __name__ == '__main__':
    cli()
