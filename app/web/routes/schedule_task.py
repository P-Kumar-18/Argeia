from datetime import datetime
from flask import current_app, request, render_template, redirect, url_for
from . import main
from ...runner import TaskRunner


@main.route("/tasks/schedule", methods=["GET", "POST"])
def schedule_task():
    if request.method == "POST":
        title = (request.form.get('title') or "").strip()
        comment = (request.form.get('comment') or "").strip() or None
        start_time_raw = request.form.get('start_time')
        end_time_raw = request.form.get('end_time')

        if not title:
            return render_template('schedule_task.html', error='Title is required.'), 400

        try:
            start_time = datetime.fromisoformat(start_time_raw)
            end_time = datetime.fromisoformat(end_time_raw)
        except (TypeError, ValueError):
            return render_template('schedule_task.html', error='Invalid date format.'), 400

        if end_time <= start_time:
            return render_template('schedule_task.html', error='End time must be after start time.'), 400

        task_runner: TaskRunner = current_app.task_runner
        task_runner.create_task(title=title, start_time=start_time, end_time=end_time, comment=comment)
        
        return redirect(url_for('main.tasks'))
    else:
        now = datetime.now().strftime('%Y-%m-%dT%H:%M')

        return render_template('schedule_task.html', now=now)