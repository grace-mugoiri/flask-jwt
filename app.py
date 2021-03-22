from flask import Flask, request, jsonify, render_template, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm
from werkzeug.security imort generate_password_hash, check_password
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
	__tablename__ = 'usertable'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	username = db.Column(db.String(20), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(256), unique=True)
# db. Creating task model using sqlalchemy
class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(70), unique=True)
	description = db.Column(db.String(100))

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


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
	task = Task.query.get(id)
	db.session.delete(task)
	db.session.commit()
	return task_schema.jsonify(task)

@app.route('/register/', methods = ["GET", "POST"])
def register():
	form = RegisterForm(request.form)
	if requested.method == "POST" and form.validate():
		hashed_password = generate_password_hash(form.password.data, method="sha256")
		new_user = User(
			name=form.name.data,
			username=form.username.data,
			email=form.email.data,
			password = hashed_password
		)
		db.session.add(new_user)
		db.session.commit()

		flash("You have successfully registered", "success")
		return redirect(url_for("login"))
	else:
		return render_template('register.html', form=form)


@app.route('/login/', methods = ["GET", "POST"])
def login():
	form = LoginForm(request.form)
	if requested.method == "POST" and form.validate():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				flash("You have successfully logged in", "success")
				session["logged_in"] = Truesession["email"] = user.email
				session["username"] = user.username
				return redirect(url_for 'home')
			else:
				flash("username or Password Incorrect", "Danger")
		return render_template('login.html', form=form)


if __name__ == "__main__":
	app.run(debug=True)
