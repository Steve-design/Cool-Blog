from flask import Flask
from flask_mail import Mail
from config import config_options
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_sqlalchemy import SQLAlchemy
from flask_simplemde import SimpleMDE

simple = SimpleMDE()

photos = UploadSet('photos',IMAGES)
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/authenticate')

    
    app.config.from_object(config_options[config_name])

    configure_uploads(app, photos)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app
