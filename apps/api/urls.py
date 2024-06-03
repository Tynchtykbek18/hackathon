from django.urls import include, path
from rest_framework import response, status, views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class HealthCheckView(views.APIView):
    def get(self, request, *args, **kwargs):
        return response.Response({"status": "ok"}, status=status.HTTP_200_OK)


urlpatterns = [
    path("healthcheck/", HealthCheckView.as_view(), name="healthcheck"),
    path("users/", include('apps.user.urls')),
    path("abituriensts/", include('apps.abiturient.urls'))
]

# token
urlpatterns += [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
