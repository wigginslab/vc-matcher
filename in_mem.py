"""
Moves the data into a sql database
"""
from datetime import datetime
import os
import pickle
import sys
from vc_matcher import *
import datetime

print datetime.datetime.now()

# For each vc, create the vc
vcs= pickle.load(open("data/vctree/opvcs.p", "rb"))

co_cograms = pickle.load(open("data/vctree/cograms.p","rb"))

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

vc_models_dic = {}
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
	vc_models_dic[vc_name] = nb_model

print datetime.datetime.now()
print 'errors %i' %(errors)