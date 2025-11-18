import logging
from notifications.channels.base import NotificationChannel

logger = logging.getLogger(__name__)


class EmailChannel(NotificationChannel):
    def send(self, to: str, subject: str, body: str, **kwargs) -> None:
        logger.info(f" [EMAIL] SEND TO === {to} === SUBJECT === {subject} === BODY === {body}")