from flask import Flask


def create_app():

    app = Flask(__name__)

    # Home
    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    # Add Task
    from app.routes.task import task_bp
    app.register_blueprint(task_bp)

    return app