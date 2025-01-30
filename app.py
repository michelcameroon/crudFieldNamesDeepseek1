from flask import Flask, request, redirect, url_for, render_template
from models import db, Student, getFieldNames

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Home page - List all students
@app.route('/')
def list_students():
    students = Student.query.all()
    fields = getFieldNames()
    return render_template('list.html', students=students, fields=fields)

# Create a new student
@app.route('/create', methods=['GET', 'POST'])
def create_student():
    fields = getFieldNames()
    if request.method == 'POST':
        data = {field: request.form[field] for field in fields}
        new_student = Student(**data)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('list_students'))
    return render_template('create.html', fields=fields)

# Update a student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    fields = getFieldNames()
    if request.method == 'POST':
        for field in fields:
            setattr(student, field, request.form[field])
        db.session.commit()
        return redirect(url_for('list_students'))
    return render_template('update.html', student=student, fields=fields)

# Delete a student
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('list_students'))
    return render_template('delete.html', student=student)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
