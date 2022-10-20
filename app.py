from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
server = 'localhost'
database = 'blog'
driver = 'ODBC Driver 17 for SQL Server'
dsn = f'mssql://@{server}/{database}?driver={driver}'
app.config['SQLALCHEMY_DATABASE_URI'] = dsn

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    
    def __repr__(self):
        return f"<User: {self.name}, {self.username}, {self.email}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email
        }

@app.route('/', methods=['GET'])
def index():
    data = db.engine.execute("SELECT * FROM [users]")
    names = [row[1] for row in data]
    return {'data' : names}

@app.route('/users', methods=['GET'])
def users():
    users = Users.query.all()
    # print(users)
    # serialized = [user.serialize() for user in users] # inline version
    # for user in users: # complicated version of for loop
    #     serialized.append(user.serialize())
        
    return {'users': [user.serialize() for user in users]}

if __name__ == '__main__':
    app.run(debug=True)