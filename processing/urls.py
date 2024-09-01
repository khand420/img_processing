from django.urls import path
from .views import UploadCSV, StatusAPI, WebhookAPIView

urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload_csv'),
    path('status/<int:request_id>/', StatusAPI.as_view(), name='status_api'),
    path('webhook/', WebhookAPIView.as_view(), name='webhook'),
]

# celery -A image_processor flower
# celery -A image_processor worker --loglevel=info
# celery -A image_processor worker --loglevel=DEBUG
# celery -A image_processor worker --pool=solo --loglevel=info



# pip freeze > requirements.txt