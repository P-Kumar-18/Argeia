from flask import current_app, request, render_template, jsonify
from datetime import datetime
from . import main
from ...runner import BehaviorRunner, TaskRunner
from ...infrastructure import TaskRepository


@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    behavior_runner: BehaviorRunner = current_app.behavior_runner
    task_runner: TaskRunner = current_app.task_runner
    task_repo: TaskRepository = current_app.task_repo

    completed_tasks = task_repo.get_n_latest_completed_tasks(5)
    upcoming_task = task_repo.get_latest_upcoming_tasks()

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        action = data.get('action')
        id = data.get('id')

        if action not in {"start", "end"}:
            return jsonify(status='error', message='Invalid action'), 400

        if id is None:
            return jsonify(status='error', message='Task id is required'), 400

        task = task_repo.get_task_by_id(id)

        if task is None:
            return jsonify(status='error', message='Task not found'), 404

        if action == 'start':
            if task.completed:
                return jsonify(status='error', message='Task is already completed'), 409
            if task.started_at is not None:
                return jsonify(status='error', message='Task already started'), 409

            when=datetime.now()
            task_runner.start_task(task=task, when=when)
            return jsonify(status='start')

        elif action == 'end':
            if task.completed:
                return jsonify(status='error', message='Task is already completed'), 409
            if task.started_at is None:
                return jsonify(status='error', message='Task must be started first'), 409

            when=datetime.now()
            task_runner.complete_task(task=task, when=when)
            return jsonify(status='end')
        
        else:
            return jsonify(status='error')

    else:    
        return render_template(
            'dashboard.html', 
            current_state=behavior_runner.current_state, 
            completed_tasks=completed_tasks, 
            upcoming_task=upcoming_task
        )