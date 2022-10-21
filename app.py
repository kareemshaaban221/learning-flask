from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql://@localhost/drinks?driver=ODBC Driver 17 for SQL Server'
db = SQLAlchemy(app)

class Drink(db.Model):
    __tablename__ = 'drinks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f"<Drink: {self.name} - Desc: {self.description}>"
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

@app.route('/drinks', methods=['GET'])
def index():
    drinks = Drink.query.all()
    
    if not len(drinks):
        return { 'message': 'No Drinks' }, 404
    else:
        return {
            'drinks': [drink.serialize for drink in drinks]
        }, 200
        
@app.route('/drinks', methods=['POST'])
def store():
    new_drink = Drink(name=request.json['name'], description=request.json['description'])
    
    try:
        db.session.add(new_drink)
        db.session.commit()
        return {
            'message': 'drink has been added successfully!',
            'drink': new_drink.serialize
        }, 201
    except Exception as e:
        return {
            'message': str(e)
        }, 500

@app.route('/drinks/<int:id>', methods=['GET'])
def show(id):
    drink = Drink.query.get(id)
    if not drink:
        return {
            'message': 'not found'
        }, 404
    else:
        return drink.serialize, 200
    
@app.route('/drinks/delete/<int:id>', methods=['DELETE'])
def delete(id):
    drink = Drink.query.get(id)
    
    if not drink:
        return {
            'message': 'not found'
        }, 404
    else:
        try:
            db.session.delete(drink)
            db.session.commit()
            return {
                'message': 'drink has been deleted successfully!',
                'drink': drink.serialize
            }, 200
        except Exception as e:
            return {
                'message': str(e)
            }, 500
            
@app.route('/drinks/update/<int:id>', methods=['PUT'])
def update(id):
    drink = Drink.query.get(id)
    
    if not drink:
        return
    else:
        

if __name__ == '__main__':
    app.run(debug=True)