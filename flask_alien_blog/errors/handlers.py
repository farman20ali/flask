from flask import Blueprint, current_app, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    with current_app.app_context():
        params=current_app.config['params']
    return render_template('errors/404.html',params=params), 404


@errors.app_errorhandler(403)
def error_403(error):
    with current_app.app_context():
        params=current_app.config['params']
    return render_template('errors/403.html',params=params), 403


@errors.app_errorhandler(500)
def error_500(error):
    with current_app.app_context():
        params=current_app.config['params']
    return render_template('errors/500.html',params=params), 500
