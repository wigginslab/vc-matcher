from datetime import datetime
from flask.ext.sqlalchemy import *
import os
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)

class NB_Model(db.Model):
	__tablename__ = "NB_Model"
	id = db.Column(db.Integer, primary_key = True)
	nb_model = db.Column(db.PickleType)