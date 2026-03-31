from django.apps import AppConfig


class BasicDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.basic_data'
    verbose_name = '基础数据'
