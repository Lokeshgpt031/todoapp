
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata')))

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=["POST", 'GET'])
def index():
    if request.method == 'POST':
        if len(request.form['content']) >= 3 and len(request.form['content']) <= 150:

            task_content = request.form['content']
            new_task = Todo(content=task_content)
        else:
            return "length of the string is less than '3' or more than '150'"


        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was an error in add or commiting the new_task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was an error in Task to Delete"


@app.route('/update/<int:id>', methods=["POST", 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was an error in Task to update"

    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
