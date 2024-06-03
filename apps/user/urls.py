from django.urls import path
from .views import UserViewSet, UserRegisterAPI, UserLoginAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", UserViewSet)

urlpatterns = [
    path('login/', UserLoginAPI.as_view(), name='user-login'),
    path('register/', UserRegisterAPI.as_view(), name='user-register'),
]

urlpatterns += router.urls
