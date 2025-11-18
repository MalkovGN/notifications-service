from django.conf import settings
from django.db import models


class UserContact(models.Model):
    class Channel(models.TextChoices):
        EMAIL = "email", "Email"
        SMS = "sms", "SMS"
        TELEGRAM = "telegram", "Telegram"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    channel = models.CharField(max_length=20, choices=Channel.choices)
    value = models.CharField(max_length=255)
    priority = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("priority",)

    def __str__(self):
        return f"{self.user_id} - {self.channel} - {self.value}"


class NotificationTemplate(models.Model):
    code = models.CharField(max_length=64, unique=True)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()

    def __str__(self):
        return self.code


class Notification(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.PROTECT)
    context = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification №{self.id} to {self.user_id}"



class NotificationAttempt(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="attempts"
    )
    channel = models.CharField(max_length=20, choices=UserContact.Channel.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)