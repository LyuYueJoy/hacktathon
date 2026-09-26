from flask import Flask


def create_app():

    app = Flask(__name__)
    app.secret_key = "hackathon-secret-key"

    # Home
    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    from app.routes.handover import handover_bp
    app.register_blueprint(handover_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
