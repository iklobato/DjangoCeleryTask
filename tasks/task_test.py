from datetime import datetime

from api.models import CeleryTask

from djangoCeleryTest.celery import app
from tasks.logica import make_distribution
from tasks.hour_checker import time_checker


@app.task(queue='default')
def save_result(object_id, result):
    obj = CeleryTask.objects.filter(id=object_id).first()
    obj.result = result
    obj.task_status = False
    obj.save()


@app.task(queue='default')
def add_task_to_queue(*args, **kwargs):
    data = kwargs.get('data')
    task_name = kwargs.get('task_name')
    print(f'Started task {task_name} processing {data}')

    chosen_queue = time_checker(time_to_check=datetime.today())
    result = make_distribution(data.split(','), chosen_queue)

    print(f'Finished task {task_name} processing {data}')

    save_result(
        object_id=kwargs.get('obj_id'),
        result=result
    )



