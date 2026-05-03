import os
from flask import Flask, redirect, url_for
from config import Config

from services.init_db_service import init_database
from services.db_service import close_db

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.upload_routes import upload_bp
from routes.analytics_routes import analytics_bp
from routes.report_routes import report_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs("database", exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["REPORT_FOLDER"], exist_ok=True)

    with app.app_context():
        init_database()

    app.teardown_appcontext(close_db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(report_bp)

    @app.route("/home")
    def home_redirect():
        return redirect(url_for("dashboard.dashboard"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)