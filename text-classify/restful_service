#!flask/bin/python
from flask import Flask,jsonify,abort
from flask import request
import WVecModel as ltcm

app = Flask(__name__)

# expensive call
classifier = ltcm.text_classifier()

@app.route('/testpath', methods=['POST'])
def create_task():
	print ('request='+str(request.json))
	if not request.json or not 'text' in request.json:
	    abort(400)

	text_input = request.json["text"]
	result = classify_text(text_input)    
	print 'result = '+result
	task = {
	    "classType": str(result),
	    "paragraph": str(text_input)
	}

	return jsonify(task), 201

def classify_text(text):

	print text
	label = classifier.classify(text)
	print label
	return label

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
