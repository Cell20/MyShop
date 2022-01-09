import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')  # creating an instance of the app

# loading custom configuration from settings
app.config_from_object('django.conf:settings', namespace='CELERY')
# celery will look for a tasks.py file in each app to load async tasks defined in it
app.autodiscover_tasks()
