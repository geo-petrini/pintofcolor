import os
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):   
    platform = os.getenv('WEB_PLATFORM')
    database_path = None
    if platform == 'HEROKU_POSTGRESQL':
        database_name ='local_db_name'
        default_database_path= "postgresql://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
        database_path = os.getenv('DATABASE_URL', default_database_path)
        if database_path.startswith('postgres:'):
            database_path = database_path.replace('postgres:', 'postgresql:') 

    if platform == 'PYTHONANYWHERE_MYSQL':
        database_path = os.getenv('DATABASE_URL', None)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create():
    db.drop_all()
    db.create_all()

class Color(db.Model):
    __tablenane__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255))
    color_name = db.Column(db.String(255))
    color_code = db.Column(db.String(8))
    ts = db.Column(db.DateTime)
    
    def __init__(self, user, color_name, color_code):
        self.user = user
        self.color_name = color_name
        self.color_code = color_code
        self.ts = datetime.datetime.now()    

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()    
        
    def update(self):
        db.session.commit()        