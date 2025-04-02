import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electronics_retail.settings')
app = Celery('electronics_retail')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()