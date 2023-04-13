from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

import os

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app():

    from main.models import models
    from main.views import views
    from main.auth import auth
    from main.admin import admin

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/fiverr_project_zjallen777'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True, 'pool_recycle': 35, 'pool_timeout' : 10, 'pool_size' : 30}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = False
    app.config['MAIL_SERVER'] = 'mail.DOMAIN.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_DEBUG'] = True
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'no-reply@DOMAIN.com'
    app.config['MAIL_PASSWORD'] = ''
    app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@DOMAIN.com'
    app.config['MAIL_MAX_EMAILS'] = 1
    app.config['MAIL_ASCII_ATTACHMENTS'] = False
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'false'
    app.config['JSON_SORT_KEYS'] = False
    app.secret_key = b"Zq1DglfU05Mkm3z30QwrZZ4KPtKSv8F4"
    


    login_manager.init_app(app)

    db.init_app(app)
    mail.init_app(app)

    app.register_blueprint(models)
    app.register_blueprint(views)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    
    return app