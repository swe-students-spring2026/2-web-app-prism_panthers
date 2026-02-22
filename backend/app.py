"""
Backend entry point for the job application tracker.
Run with: python app.py
"""
from flask import Flask
from dotenv import load_dotenv

from config import Config
from extensions import init_extensions


def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/static",
    )
    app.config.from_object(Config)

    init_extensions(app)

    from modules.auth_profile.routes import auth_profile_bp
    from modules.listings.routes import listings_bp
    from modules.applications.routes import applications_bp

    app.register_blueprint(auth_profile_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(applications_bp)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
