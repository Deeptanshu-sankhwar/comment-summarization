from flask import Flask
import os
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route("/summary", methods=['GET', 'POST'])
def summary():
	message = request.get_json(force=True)
	name = message['name']
	os.system('python3 scraper.py ' + name)
	from summary_generation import main
	summary = main(1)
	
	response = {
		'summary' : summary
	}
	return jsonify(response)