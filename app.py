from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = "taskmaster_secret"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f'Task: {self.id}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task adding succesfully!', 'success')
            return redirect('/')
        except:
            flash('There was an issue adding the task', 'danger')
            return redirect('/')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Task deleting succesfully!', 'success')
        return redirect('/')
    except:
        flash('There was an issue deleting the task', 'danger')
        return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            flash('Task updated succesfully!', 'success')
            return redirect('/')
        except:
            flash('There was an issue updating the task', 'danger')
            return redirect('/')
    else:
        return render_template('update.html', task=task)

@app.route('/complete/<int:id>')
def complete(id):
    task = Todo.query.get_or_404(id)
    try:
        task.completed = 1 
        db.session.commit()
        flash('Task marked as completed!', 'success')
        return redirect('/')
    except:
        flash('There was an issue marking the task as completed', 'danger')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)