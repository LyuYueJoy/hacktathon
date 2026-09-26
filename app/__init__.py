from flask import Flask


def create_app():

    app = Flask(__name__)
    app.secret_key = "hackathon-secret-key"  # fine for a demo, don't reuse for anything real

    # Home
    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    # Add Task
    from app.routes.task import task_bp
    app.register_blueprint(task_bp)

    # Auth
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app