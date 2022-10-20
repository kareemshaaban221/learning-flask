from flask import Flask, render_template, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# application run
app = Flask(__name__)

# database configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

# Home Route
@app.route('/', methods=['POST', 'GET'])

# Home Controller
def index():
    if request.method == 'POST':
        text = request.form['task']
        new_task = Task(content=text)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There is an error in database engine!"
            
    else:
        return render_all_tasks()
    
###########################################################################################################
    
# Delete Route
@app.route('/delete/<int:id>')

# Delete Controller
def delete(id):
    task = Task.query.get_or_404(id)
    
    try:
        db.session.delete(task)
        db.session.commit()
        
        return redirect('/')
    except:
        return "There was an error in deleting!"

@app.route('/update/<int:id>', methods=['POST', 'GET'])

# Update Controller
def update(id):
    task = Task.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['task']
        
        try:
            db.session.commit()
            
            return render_all_tasks()
        except:
            return 'There is an error in updating!'
    else:
        return render_template('update.html', task=task)
    

# Helpers
def render_all_tasks():
    tasks = Task.query.order_by(Task.created_at).all()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)