from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/restapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# db. Creating task model using sqlalchemy
class Task(db.Model):
	id = db.column(db.Integer, primary_key=True)
	title = db.column(db.String(70), unique=True)
	description = db.column(db.Strng(100))

	def __init__(self, title, description):
		self.title = title
		self.description = description

db.create_all()

# creating task model using Marshmallow
class TaskSchema(ma.Schema):
	class Meta:
		fields = ("id", "title", "description")

# generating object of TaskSchema for single object and for multiple object
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route('/', methods=['GET'])
def index():
	return jsonify({'msg': 'Works'})


@app.route('/tasks', methods=['POST'])
def create_task():
	title = request.json['title']
	description = request.json['description']

	new_task = Task(title, description)

	db.session.add(new_task)
	db.session.commit()

	return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
	all_tasks = Task.query.all()
	result = tasks_schema.dump(all_tasks)
	return jsonify(result)


@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
	task = Task.query.get(id)
	return task_schema.jsonify(task)

@app.route('/tasks/<id>')
def update_task(id):
	task = Taks.query.get(id)
	title = request.json['title']
	description = request.json['description']

	task.title = title
	task.description = description

	db.session.commit()
	return task_schema.jsonify(task)





