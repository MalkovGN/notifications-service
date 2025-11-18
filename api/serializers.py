from rest_framework import serializers
from notifications.models import Notification


class NotificationCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    template_code = serializers.CharField()
    context = serializers.JSONField(required=False)


class NotificationDetailSerializer(serializers.ModelSerializer):
    attempts = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            "id",
            "user",
            "template",
            "context",
            "status",
            "created_at",
            "attempts",
        )

    def get_attempts(self, obj):
        qs = obj.attempts.all().order_by("created_at")
        return [
            {
                "channel": a.channel,
                "status": a.status,
                "error_message": a.error_message,
                "created_at": a.created_at,
            }
            for a in qs
        ]
