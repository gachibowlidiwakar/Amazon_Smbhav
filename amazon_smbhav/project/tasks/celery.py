from celery import Celery
from celery.schedules import crontab

# Set up Celery and Redis as the message broker
app = Celery('tasks', broker='redis://localhost:6379/0')

# Explicitly import tasks
from tasks.tasks import fetch_pdfs

# Define periodic tasks
app.conf.beat_schedule = {
    'fetch-pdfs-every-1-minute': {
        'task': 'tasks.tasks.fetch_pdfs',  # Fully qualified task name
        'schedule': crontab(minute='*/1'),
    },
}

app.conf.timezone = 'UTC'
