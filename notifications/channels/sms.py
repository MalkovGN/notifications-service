import logging
from notifications.channels.base import NotificationChannel

logger = logging.getLogger(__name__)


class SMSChannel(NotificationChannel):
    def send(self, to: str, subject: str, body: str, **kwargs) -> None:
        logger.info(f" [SMS] SEND TO === {to} === BODY === {body}")