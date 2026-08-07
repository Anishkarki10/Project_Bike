from flask import Flask, Blueprint
from app.auth import admin_required


def test_admin_page_redirects_guest():
    app = Flask(__name__)
    app.secret_key = 'test'
    bp = Blueprint('admin', __name__, url_prefix='/admin')

    @bp.route('/login')
    def login():
        return 'login'

    @bp.route('/private')
    @admin_required
    def private():
        return 'private'

    app.register_blueprint(bp)
    client = app.test_client()
    response = client.get('/admin/private')
    assert response.status_code == 302
    assert '/admin/login' in response.location
