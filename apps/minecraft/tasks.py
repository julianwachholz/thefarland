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
        '-X', 'stuff', '{cmd}\r'.format(command),
    ]
    subprocess.call(args)
