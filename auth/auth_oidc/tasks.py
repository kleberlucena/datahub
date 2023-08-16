from allauth.socialaccount.models import SocialAccount
from celery import shared_task
from celery_progress.backend import ProgressRecorder
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def task_update_social_account_from_user(self):
    progress_recorder = ProgressRecorder(self)
    accounts = SocialAccount.objects.all()
    if accounts:
        i = 0
        for account in accounts:
            if account.user:
                account.uid = account.user.username
                account.save()
        total_percents = ((i / len(accounts)) * 100)
        progress_recorder.set_progress(i + 1, 10, f'Concluído {total_percents}%')
        logger.info('Conta social atualizada - {}'.format(account.uid))
    else:
        progress_recorder.set_progress(0, 0, f'Concluído 100%')
        logger.info('Atualização de contas finalizado - total: {}'.format(len(accounts)))