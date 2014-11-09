from thefarland.celery import app as celery_app
from apps.accounts.models import User


@celery_app.task(ignore_result=True)
def verification_code(user_id):
    """
    Tell a user their verification code via Minecraft.

    """
    user = User.objects.get(id=user_id)
