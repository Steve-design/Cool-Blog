from app import create_app,db
from flask_script import Manager,Server
from app.models import *
from  flask_migrate import Migrate, MigrateCommand

app = create_app('development')