from rad.celery import app as celery_app
import os
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
__all__ = ['celery_app',]