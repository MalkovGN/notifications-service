import logging

from django.db import transaction
from django.template import Context, Template

from notifications.models import Notification, UserContact, NotificationAttempt
from notifications.channels import get_channel_sender

logger = logging.getLogger(__name__)


def render_template(template, context: dict) -> tuple[str, str]:
    subject = Template(template.subject or "").render(Context(context))
    body = Template(template.body).render(Context(context))
    return subject, body


def send_notification(notification_id: int) -> None:
    notification = Notification.objects.select_related("template", "user").get(id=notification_id)
    contacts = UserContact.objects.filter(user=notification.user, is_active=True).order_by("priority")

    subject, body = render_template(notification.template, notification.context)

    sent = False

    for contact in contacts:
        sender = get_channel_sender(contact.channel)
        try:
            sender.send(contact.value, subject, body)
            with transaction.atomic():
                NotificationAttempt.objects.create(
                    notification=notification,
                    channel=contact.channel,
                    status=NotificationAttempt.Status.SUCCESS,
                )
                notification.status = Notification.Status.SENT
                notification.save(update_fields=["status", "updated_at"])
            sent = True
            break

        except Exception as e:
            last_error = str(e)
            logger.error(last_error)
            NotificationAttempt.objects.create(
                notification=notification,
                channel=contact.channel,
                status=Notification.Status.FAILED,
                error_message=last_error,
            )

    if not sent:
        notification.status = Notification.Status.FAILED
        notification.save(update_fields=["status", "updated_at"])