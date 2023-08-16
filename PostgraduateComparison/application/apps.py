from django.apps import AppConfig
from django.contrib.admin import apps

class MyAdminSite(apps.AdminConfig):
    default_site = 'application.admin.MyAdminSite'

class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'