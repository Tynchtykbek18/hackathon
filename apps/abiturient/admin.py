from django.contrib import admin
from apps.abiturient.models import Department, Request, Exam

admin.site.register(Exam)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'department')
    list_display_links = ('id', 'email')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
