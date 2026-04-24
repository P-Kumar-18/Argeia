from datetime import datetime
from flask import current_app, request, render_template, url_for, redirect
from . import main
from ...infrastructure import TaskRepository

@main.route("/task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    action = request.form.get('action')

    task_repo: TaskRepository = current_app.task_repo
    task = task_repo.get_task_by_id(task_id)

    if task is None:
        return "Task not found", 404

    if action is None:
        title = task.title
        comment = task.comment
        now = datetime.now().strftime('%Y-%m-%dT%H:%M')
        task_completed = task.completed

        return render_template(
            'edit_task.html',
            title=title, 
            comment=comment,
            now=now,
            task_completed=task_completed
        )
    
    if action == "update":
        new_title = (request.form.get('title') or task.title).strip()
        new_comment = request.form.get('comment') or task.comment

        start_time_raw = request.form.get('start_time')
        end_time_raw = request.form.get('end_time')

        try:
            new_start_time = datetime.fromisoformat(start_time_raw) if start_time_raw else task.scheduled_for_start
            new_end_time = datetime.fromisoformat(end_time_raw) if end_time_raw else task.scheduled_for_end
        except ValueError:
            return render_template(
                'edit_task.html',
                title=task.title,
                comment=task.comment,
                error='Invalid date format.'
            ), 400

        if new_end_time <= new_start_time:
            return render_template(
                'edit_task.html',
                title=task.title,
                comment=task.comment,
                error='End time must be after start time.'
            ), 400
        
        task_repo.update_task(task_id, title=new_title, comment=new_comment, start_time=new_start_time, end_time=new_end_time)

        return redirect(url_for('main.tasks'))

    if action == "delete":
        task_repo.delete_task(task_id)

        return redirect(url_for('main.tasks'))

    return redirect(url_for('main.tasks'))