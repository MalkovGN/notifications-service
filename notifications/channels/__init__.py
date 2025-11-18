from notifications.channels.email import EmailChannel
from notifications.channels.sms import SMSChannel
from notifications.channels.telegram import TelegramChannel
from notifications.channels.base import NotificationChannel


def get_channel_sender(channel: str) -> NotificationChannel:
    if channel == "email":
        return EmailChannel()
    if channel == "sms":
        return SMSChannel()
    if channel == "telegram":
        return TelegramChannel()
    raise ValueError(f"Unknown channel {channel}")
