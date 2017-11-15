from __future__ import absolute_import
from __future__ import absolute_import, unicode_literals
from celery import task
import os


@task()
def task_number_one():
    os.system("./manage.py test")
