#!/usr/bin/env python3
 

import json
from flask import Flask


 
from utils import bcrypt, getUUID,mail
from models import getJson, login_manager,db
 

    


login_manager.login_view='users.login'
login_manager.login_message='you need login to access this page'
login_manager.login_message_category='info'

with open( 'config.json', 'r') as c:
    params = json.load(c)["params"]

# params=[]
   
def create_app():
    secret_key=getUUID() 
    app = Flask("Clean Blog")
    local_server = params["local_server"]
    if (local_server):
        app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    app.config['SQLALCHEMY_BINDS'] = {
    # Configuration for the second database
    'site_db': 'sqlite:///site.db'}
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        mail_params=getJson('mail')
        admin_params=getJson('admin')
    app.config.update(
    params=params,
    mail_params=mail_params,
    admin_params=admin_params,
    SECRET_KEY=secret_key,
    MAIL_SERVER=mail_params['mail_server'],
    MAIL_PORT=mail_params['mail_port'],
    MAIL_USE_SSL=mail_params['mail_ssl'],
    MAIL_USERNAME=mail_params['gmail-user'],
    MAIL_PASSWORD=mail_params['gmail-password']
    )
    mail.init_app(app) 
    bcrypt.init_app(app)
    from users.routes import users
    from posts.routes import posts
    from main.routes import main
    from admin.routes import admin
    from errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(errors)
    return app

 

 










 
 












