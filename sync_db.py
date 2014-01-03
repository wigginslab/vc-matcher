"""
Moves the data into a sql database
"""
from datetime import datetime
from flask.ext.sqlalchemy import *
import os
from flask import Flask
from models.company import Company,VC,Trigram,Cogram, db
import pickle
import sys
from vc_matcher import *
import datetime
db.create_all()

if len(sys.argv) > 1:
	arg = sys.argv[1]
	if arg == "drop":
		db.drop_all()
		sys.exit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)

# For each vc, create the vc
vcs= pickle.load(open("data/vctree/opvcs.p", "rb"))

co_cograms = pickle.load(open("data/vctree/cograms.p","rb"))

print datetime.datetime.now()
# get all companies for each vc
vc_cos = {}
for vc in vcs:
	vc_name = vc[0]
	cos = vc[2]
	vc_cos[vc_name] = [co[0] for co in cos]

cogram_dic = {}
#get all cograms for each company
for cogram in co_cograms:
	company_name = cogram[0]
	cograms = cogram[1]
	cogram_dic[company_name] = cograms

vc_num = 1
errors = 0
for vc in vcs:
	vc_url = vc[0]
	vc_name = vc[1]
	vc_companies = vc_cos[vc_url]
	yes_cograms = []
	# get cograms used in vc companies
	no_cograms = []
	for company in vc_companies:
		try:
			yes_cograms.append(cogram_dic[company])
		except:
			errors = errors + 1

	# get equal cograms not used in vc companies
	for i in range(len(vc_companies)):
		company = cogram_dic.keys()[i]
		if company not in vc_companies:
			no_cograms.append(cogram_dic[company])
	nb_model = build_model(yes_cograms,no_cograms)
	new_VC = VC(name=vc_name,url=vc_url, nb_model=nb_model)
	db.session.add(new_VC)
	db.session.commit()
	print vc_num
	vc_num = vc_num + 1

db.session.close()

print datetime.datetime.now()
print 'errors %i' %(errors)
