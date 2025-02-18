import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrator.settings')

app = Celery('integrator')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'close-aplication': {
        'task': 'applications.tasks.CloseApplication',
        'schedule': crontab(minute='*/60'), #Каждый час
    },
    'comments-from-emails': {
        'task': 'applications.tasks.CommentsFromEmails',
        'schedule': crontab(minute='*/5'), #Каждые 5 минут
    }
}
