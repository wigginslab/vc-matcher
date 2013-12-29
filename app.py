import os
from flask import Flask, request, Response, render_template,jsonify
import datetime
import os
import re
from werkzeug.wsgi import SharedDataMiddleware
import json
from vc_matcher import match_vc

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/get/vcs/<int:page>',methods=['POST', 'GET'])
def get_vcs(page):
	"""
	Match startup description with vcs
	"""
	# startup description
	desc = request.form['description']
	vc_lists = match_vc(desc, page)
	return Response(json.dumps(vc_lists), status=200, mimetype="application/json")

# store assets files on server for now
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__':
	app.run(debug=True, port=8000)
