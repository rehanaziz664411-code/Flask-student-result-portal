from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, default=100)
    grade = db.Column(db.String(5))

# --- GRADE CALCULATION LOGIC ---
def calculate_grade(score):
    if score >= 80: return "A+"
    elif score >= 70: return "A"
    elif score >= 60: return "B"
    elif score >= 50: return "C"
    elif score >= 40: return "D"
    else: return "Fail"

# --- ROUTES ---
@app.route('/')
def index():
    search = request.args.get('search')
    if search:
        # Search by Name or Roll Number
        students = Student.query.filter((Student.name.contains(search)) | (Student.roll_no.contains(search))).all()
    else:
        students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        score = int(request.form['marks'])
        
        new_student = Student(
            name=name, 
            roll_no=roll, 
            marks=score, 
            grade=calculate_grade(score)
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Creates the database file automatically
    app.run(debug=True)