from django.apps import AppConfig
from django.conf import settings

class LabelinterfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Labelinterface'

class HomepageConfig(AppConfig):
    name = 'homepage'