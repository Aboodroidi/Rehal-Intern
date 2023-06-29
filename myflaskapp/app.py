from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(80))
    students = db.relationship('Student', backref='school_class', lazy=True)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(80))
    students = db.relationship('Student', backref='country', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    name = db.Column(db.String(80))
    date_of_birth = db.Column(db.DateTime)

    def __repr__(self):
        return '<Student %r>' % self.name

@app.route('/')
def index():
    students = Student.query.all()
    countries = Country.query.all()

    # Calculating statistics
    student_per_class = db.session.query(SchoolClass.id, SchoolClass.class_name, func.count(Student.id)).join(Student).group_by(SchoolClass.id).all()
    student_per_country = db.session.query(Country.country_name, func.count(Student.id)).join(Student).group_by(Country.id).all()
    average_age = db.session.query(func.avg(func.julianday(datetime.now()) - func.julianday(Student.date_of_birth))/365.25).scalar()

    return render_template('index.html', students=students, countries=countries, student_per_class=student_per_class, student_per_country=student_per_country, average_age=average_age)


@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    dob = request.form.get('dob')  # date_of_birth
    dob = datetime.strptime(dob, '%Y-%m-%d')  # convert string to datetime object
    class_name = request.form.get('class_id')
    country_name = request.form.get('country_name')

    # Get or create SchoolClass and Country
    school_class = SchoolClass.query.filter_by(class_name=class_name).first()
    if not school_class:
        school_class = SchoolClass(class_name=class_name)
        db.session.add(school_class)
        db.session.commit()

    country = Country.query.filter_by(country_name=country_name).first()
    if not country:
        country = Country(country_name=country_name)
        db.session.add(country)
        db.session.commit()

    student = Student(name=name, date_of_birth=dob, class_id=school_class.id, country_id=country.id)
    db.session.add(student)
    db.session.commit()

    return redirect(url_for('index'))  # redirect to the main page

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # drop all tables
        db.create_all()  # create tables
    app.run(debug=True)
