from datetime import datetime
from flask.ext.sqlalchemy import *
import os
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)


class Trigram(db.Model):
	__tablename__ = "Trigram"
	id = db.Column(db.Integer, primary_key = True)
	word_one = db.Column(db.String)
	word_two = db.Column(db.String)
	word_three = db.Column(db.String)
	frequency = db.Column(db.Integer)