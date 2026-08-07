import os
from flask import Flask, render_template
from app.models.database import Database
from app.routes.public import PublicRoutes
from app.routes.admin import AdminRoutes
import config


def create_app(testing=False):
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    app.config['TESTING'] = testing
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    app.config['BIKE_UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads', 'bikes')
    os.makedirs(app.config['BIKE_UPLOAD_FOLDER'], exist_ok=True)

    if not testing:
        with app.app_context():
            Database.ensure_database()
            Database.create_tables()

    public_routes = PublicRoutes()
    admin_routes = AdminRoutes()
    app.register_blueprint(public_routes.register())
    app.register_blueprint(admin_routes.register())

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('notfound.html'), 404

    return app
