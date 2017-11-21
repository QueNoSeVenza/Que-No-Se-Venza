from __future__ import absolute_import
from __future__ import absolute_import, unicode_literals
from celery import task



@task()
def task_number_one():
    f = open('helloworld.txt','w')
    f.write('hello world')
    f.close()
