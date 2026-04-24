from flask import Flask
from flask_wtf import CSRFProtect
from .infrastructure import Database, TaskRepository, TransitionRepository, WindowRepository, get_default_path
from .runner import TaskRunner, BehaviorRunner, WindowManager


def create_app():
    app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

    app.config["SECRET_KEY"] = "dev"
    csrf = CSRFProtect(app)

    # Database
    db_path = get_default_path()
    Database(db_path=db_path)

    # Repositories
    task_repo = TaskRepository(db_path=db_path)
    transition_repo = TransitionRepository(db_path=db_path)
    window_repo = WindowRepository(db_path=db_path)

    # Runners
    behavior_runner = BehaviorRunner(transition_repository=transition_repo, window_repository=window_repo)
    task_runner = TaskRunner(behavior_runner=behavior_runner, task_repo=task_repo)
    window_manager = WindowManager(repository=window_repo)

    # Attach to app
    app.task_runner = task_runner
    app.task_repo = task_repo
    app.transition_repo = transition_repo
    app.behavior_runner = behavior_runner

    from .web.routes import main
    app.register_blueprint(main)

    return app