from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(80))
    students = db.relationship('Student', backref='class', lazy=True)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(80))
    students = db.relationship('Student', backref='country', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    name = db.Column(db.String(80))
    date_of_birth = db.Column(db.DateTime)

    def __repr__(self):
        return '<Student %r>' % self.name

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    dob = request.form.get('dob')  # date_of_birth
    dob = datetime.strptime(dob, '%Y-%m-%d')  # convert string to datetime object
    class_id = request.form.get('class_id')
    country_id = request.form.get('country_id')
    
    student = Student(name=name, date_of_birth=dob, class_id=class_id, country_id=country_id)
    db.session.add(student)
    db.session.commit()

    return 'Student added successfully'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)
