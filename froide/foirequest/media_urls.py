from django.urls import path

from .views import auth_message_attachment


urlpatterns = [
    path('<int:message_id>/<path:attachment_name>', auth_message_attachment,
            name='foirequest-auth_message_attachment'),
]
