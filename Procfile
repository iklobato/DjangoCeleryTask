web: gunicorn --bind :8000 djangoCeleryTest.settings.wsgi:application
celery_worker: celery worker -A djangoCeleryTest.settings.celery.app --concurrency=1 --loglevel=INFO -n worker.%%h
celery_beat: celery beat -A djangoCeleryTest.settings.celery.app --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=INFO