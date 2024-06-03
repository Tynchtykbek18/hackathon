from django.urls import path
from .views import DepartmentList, RequestCreateAPI, RequestListAPI, RequestDetailAPI

urlpatterns = [
    path('requests/', RequestListAPI.as_view(), name='request-list'),
    path('requests/<int:pk>/', RequestDetailAPI.as_view(), name='request-detail'),
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('request-create/', RequestCreateAPI.as_view(), name='request-create'),
]
