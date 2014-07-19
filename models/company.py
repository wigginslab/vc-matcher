from datetime import datetime
from flask.ext.sqlalchemy import *
import os
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
print app.config['SQLALCHEMY_DATABASE_URI']

db = SQLAlchemy(app)


company_vc= db.Table('Companies_to_VCs',
	db.Column('company_id', db.Integer, db.ForeignKey('Company.id')),
    db.Column('vc_id', db.Integer, db.ForeignKey('VC.id'))
)

class Company(db.Model):
	__tablename__ = "Company"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	url = db.Column(db.String)
	venture_capitalists = db.relationship('VC', secondary=company_vc,
    	backref=db.backref('Company', lazy='dynamic'))

class VC(db.Model):
	__tablename__ = "VC"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	url = db.Column(db.String)
	nb_model = db.Column(db.PickleType)

	def __str__(self):
		return "%s" % (self.url)

	def __repr__(self):
		return "%s" % (self.url)


class Cogram(db.Model):
	__tablename__ = "Cogram"
	id = db.Column(db.Integer, primary_key = True)
	word_one = db.Column(db.String)
	word_two = db.Column(db.String)
	company_url = db.Column(db.String)
	company_name =db.Column(db.String)

class Trigram(db.Model):
	__tablename__ = "Trigram"
	id = db.Column(db.Integer, primary_key = True)
	word_one = db.Column(db.String)
	word_two = db.Column(db.String)
	word_three = db.Column(db.String)
	company_url = db.Column(db.String)
	company_name = db.Column(db.String)
