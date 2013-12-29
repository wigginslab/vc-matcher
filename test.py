import naive_bayes as nb
from models.company import *
import pickle
import datetime
import sys
import os


print datetime.datetime.now()
text = "Anyone can create an account and start explaining rap. Highlight any line to explain it yourself, suggest changes to existing explanations, and put up your favorite new songs."

text_2="Coupons.com is a provider of digital coupons, including online printable, coupon codes, save to loyalty card and mobile promotions. The company's products include Coupons.com as well as Grocery iQ and Coupons.com mobile applications."
vcs= db.session.query(VC).filter("id >= 0 AND id <=50").all()
print 'done query'
vc_names = []
vc_urls = []
percent = []
for vc in vcs:
	vc_name = vc.name
	vc_url = vc.url
	vc_model = pickle.loads(vc.nb_model)
	result = nb.test(text=text_2, model=vc_model)
	if result >= .55:
		percent.append(result)
		vc_names.append(vc_name)
		vc_urls.append(vc_url)

print percent
print vc_names
print datetime.datetime.now()
# print results