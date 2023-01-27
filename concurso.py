from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bdconcurso'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carnet = db.Column(db.String(6), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    career = db.Column(db.String(100), nullable=False)
    poetry_genre = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.Date, default=datetime.now(), nullable=False)
    declamation_date = db.Column(db.Date,nullable=False)

    def __init__(self, carnet, name, address, gender, phone, birthdate, career, poetry_genre):
        self.carnet = carnet
        self.name = name
        self.address = address
        self.gender = gender
        self.phone = phone
        self.birthdate = birthdate
        self.career = career
        self.poetry_genre = poetry_genre

@app.route('/')
def index():
    return redirect('/register')
    

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    carnet = data.get('carnet')
    name = data.get('name')
    address = data.get('address')
    gender = data.get('gender')
    phone = data.get('phone')
    birthdate = data.get('birthdate')
    career = data.get('career')
    poetry_genre = data.get('poetry_genre')

    if len(carnet) != 6 or '0' in carnet or carnet[0] != 'A' or carnet[2] != '5' or carnet[-1] not in ('1', '3', '9'):
        return jsonify({'error': 'Invalid carnet'}), 400

    if birthdate is None:
        return jsonify({'error': 'Missing birthdate'}), 400
    birthdate_obj = datetime.strptime(birthdate, '%Y/%m/%d')
    if (birthdate_obj + timedelta(days=365*17)).date() > datetime.now().date():
        return jsonify({'error': 'Invalid birthdate'}), 400


    form_data = FormData(carnet, name, address, gender, phone, birthdate_obj, career, poetry_genre)
    db.session.add(form_data)
    db.session.commit()
    return jsonify({'message': 'Form data registered successfully'}), 201


@app.route('/inscripcion', methods=['POST'])
def inscription():
  
    form_data = request.get_json()
    form_data = FormData(carnet=form_data['carnet'], 
                         name=form_data['name'], 
                         address=form_data['address'], 
                         gender=form_data['gender'], 
                         phone=form_data['phone'], 
                         birthdate=datetime.strptime(form_data['birthdate'], '%Y/%m/%d'),
    career=form_data['career'],
    genre=form_data['genre'],
    date_inscription=datetime.now())

    return jsonify({'message': 'Inscripción exitosa'})


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
