from celery import shared_task
from notifications.services import send_notification


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_task(self, notification_id: int):
    try:
        send_notification(notification_id)
    except Exception as exc:
        raise self.retry(exc=exc)
