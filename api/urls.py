from django.urls import path
from .views import NotificationCreateView, NotificationDetailView

urlpatterns = [
    path("notifications/", NotificationCreateView.as_view(), name="notification-create"),
    path("notifications/<int:pk>/", NotificationDetailView.as_view(), name="notification-detail"),
]
