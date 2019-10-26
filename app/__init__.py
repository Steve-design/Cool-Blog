from flask import Flask
from flask_mail import Mail
from config import config_options
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_sqlalchemy import SQLAlchemy
from flask_simplemde import SimpleMDE
