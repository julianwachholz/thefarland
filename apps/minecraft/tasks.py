import subprocess

from thefarland.celery import app as celery_app
from apps.accounts.models import User


@celery_app.task(ignore_result=True)
def minecraft_cmd(command):
    """
    Run a minecraft console command.

    """
    args = [
        'screen', '-p', '0', '-S', 'minecraft',
        '-X', 'stuff', '{}\r'.format(command),
    ]
    subprocess.call(args)


@celery_app.task
def minecraft_cmd_return(command):
    """
    Run a minecraft console command.

    """
    args = [
        '/usr/bin/minecraft', 'cmd', '{}'.format(command),
    ]
    output = subprocess.check_output(args)
    return output.decode('utf-8')
