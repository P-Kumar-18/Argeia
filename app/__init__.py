from flask import Flask
from .infrastructure import Database, get_default_path


def create_app():
    app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

    app.config["SECRET_KEY"] = "dev"

    db_path = get_default_path()
    Database(db_path=db_path)

    from .web.routes import main
    app.register_blueprint(main)

    return app