from flask import current_app, render_template
from . import main
from ...infrastructure import TaskRepository


@main.route("/tasks")
def tasks():
    task_repo: TaskRepository = current_app.task_repo

    tasks = task_repo.get_all_tasks()

    return render_template(
        'tasks.html', 
        tasks=tasks
    )