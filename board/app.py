from flask import Flask, request, render_template, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_caching import Cache


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/board"
mongo = PyMongo(app)

app.config["CACHE_TYPE"] = "redis"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"

cache = Cache(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/add', methods=['post', 'get'])
def login():
	name, title, message, comments = request.form.get('name'), request.form.get('title'), request.form.get('message'), request.form.get('comments')

	if request.method == 'POST':
		id = mongo.db.board.insert({'name': name, 'title': title, 'message': message, 'comments': comments})

	if name and title and message:
		message = "Correct"
	else:
		message = 'No Correct'

	return render_template('index.html', message=message)

@app.route('/add/<id>', methods=['POST'])
def add_comments(id):
	comments = request.form.get('comments')
	name = mongo.db.board.find_one({'_id': ObjectId(id)})
	
	if request.method == 'POST':
		id = mongo.db.board.insert({'comments': comments})
	if comments:
		message = " Add comments"
	else:
		message = "No add comments"

	return render_template('coment.html', message=message)


@app.route('/names')
def names():
	names = mongo.db.board.find()
	#resp = dumps(names)

	return render_template('index.html', names=names)

@app.route('/names/<id>')
def name(id):
	name = mongo.db.board.find_one({'_id': ObjectId(id)})
	resp = dumps(name)
	return resp

@app.route('/delete/<id>', methods=['DELETE'])
def delete_board(id):
	mongo.db.board.delete_one({'_id': ObjectId(id)})
	resp = jsonify("User delete board")
	resp.status_code = 200 
	return resp



@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'not_found' + request.url
	}
	resp = jsonify(message)
	resp.status_code = 404
	return resp


if __name__ == "__main__":
	app.run(debug=True) 