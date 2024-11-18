from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'task': task.task} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task_content = data.get('task')
    if not task_content:
        return jsonify({'error': 'Task content is required'}), 400

    new_task = Task(task=task_content)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'id': new_task.id, 'task': new_task.task}), 201

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)