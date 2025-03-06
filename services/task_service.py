from dao.task_dao import get_all_tasks, add_task, update_task_status, delete_task, update_task
from models.task import Task

def get_tasks():
    return get_all_tasks()

def create_task(title, description):
    add_task(title, description)

def toggle_task_status(task_id, completed):
    update_task_status(task_id, completed)

def remove_task(task_id):
    delete_task(task_id)

def edit_task(task_id, title, description):
    update_task(task_id, title, description)
