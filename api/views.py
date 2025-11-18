from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import NotificationCreateSerializer, NotificationDetailSerializer
from notifications.models import Notification, NotificationTemplate
from notifications.tasks import send_notification_task


class NotificationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NotificationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        template = get_object_or_404(
            NotificationTemplate, code=data["template_code"]
        )

        notification = Notification.objects.create(
            user_id=data["user_id"],
            template=template,
            context=data.get("context") or {},
        )

        send_notification_task.delay(notification.id)

        return Response({"id": notification.id}, status=status.HTTP_201_CREATED)


class NotificationDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=pk)
        serializer = NotificationDetailSerializer(notification)
        return Response(serializer.data)
