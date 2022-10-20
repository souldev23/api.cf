import json
from unittest import result
from flask import Blueprint, request

from .models.task import Task
from .responses import response, not_found, bad_request
from app.models import task
from .schemas import task_schema, tasks_schema, param_task

api_v1 = Blueprint('api',__name__, url_prefix='/api/v1')

def set_task(main_func):
    def find_task(*args, **kwargs):
        id_task = kwargs.get('id_task', 0)
        print("Decoramos para obtener la tarea {}".format(id_task))
        task = Task.query.filter_by(id=id_task).first()
        if task is None:
            return not_found()
        return main_func(task)
    find_task.__name__ = main_func.__name__
    return find_task


@api_v1.route('/tasks', methods=['GET'])
def get_tasks():
    page = int(request.args.get('page', 1))

    #tasks = Task.query.all()
    resp = Task.get_by_page(page, sort='desc')
    tasks = resp[0]
    """ Deprecated by Marshmallow
    return response([
        task.serialize() for task in tasks
    ])"""
    return(tasks_schema.dump(tasks))

@api_v1.route('/tasks/<id_task>', methods=['GET'])
@set_task
def get_task(task):
    return response(task_schema.dump(task))

@api_v1.route('/tasks', methods=['POST'])
def create_task():
    body = request.get_json(force=True)
    print(body)
    """Deprecated by Marshmallow
    if body.get('title') is None or len(body.get('title'))>50:
        return bad_request()
    if body.get('description') is None:
        return bad_request()
    if body.get('deadline') is None:
        return bad_request()"""
    result_error = param_task.validate(body)
    if(result_error):
        print(result_error)
        return bad_request()
    task = Task.new(body['title'], body['description'], body['deadline'])
    result = task.save()
    if result[0]:
        resp = {'message': result[1], 'Task added': task_schema.dump(task)}
        return response(resp)
    else:
        return response({'message': result[1], 'error': result[2]}, False)


@api_v1.route('/tasks/<id_task>', methods=['PUT'])
@set_task
def update_task(id_task):
    task = Task.query.filter_by(id=id_task).first()
    if task is None:
        return not_found()
    
    body = request.get_json(force=True)
    task.title = body.get('title', task.title)
    task.description = body.get('description', task.description)
    task.deadline = body.get('deadline', task.deadline)
    result = task.save()
    if result[0]:
        resp = {'message': result[1], 'Task edited': task_schema.dump(task)}
        return response(resp)
    else:
        return response({'message': result[1], 'error': result[2]}, False)

@api_v1.route('/tasks/<id_task>', methods=['DELETE'])
@set_task
def delete_task(task):
    result = task.delete()
    if result[0]:
        resp = {'message': result[1], 'Task deleted': task_schema.dump(task)}
        return response(resp)
    else:
        return response({'message': result[1], 'error': result[2]}, False)