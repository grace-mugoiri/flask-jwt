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
