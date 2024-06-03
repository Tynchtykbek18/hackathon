from .views import CreateAPIView
from django.urls import path


urlpatterns = [
    path('create/', CreateAPIView.as_view()),
]