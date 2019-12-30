from setuptools import setup

setup(
    name='snapshotanalyzer',
    version='0.1',
    author='me',
    author_email='christiantcbell@gmail.com',
    description='Snapshot analyzer for ec2 instances',
    license='GPLv3+',
    packages=['find_ec2_instances'],
    url='https://github.com/ChristianBell1995/cloudguru-snapshot',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        find_ec2_instances=find_ec2_instances.find_ec2_instances:cli
    '''
)
