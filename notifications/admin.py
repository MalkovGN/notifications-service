from django.contrib import admin
from notifications.models import UserContact, NotificationTemplate, Notification, NotificationAttempt


admin.site.register(UserContact)
admin.site.register(NotificationTemplate)
admin.site.register(Notification)
admin.site.register(NotificationAttempt)

