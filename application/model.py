from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



class Admin(db.Model):
    __tablename__ = 'admin'
    a_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String)
    gender = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Student(db.Model):
    __tablename__ = 'student'
    roll = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String)
    gender = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    degree = db.Column(db.String, nullable=False)
    dept_code = db.Column(db.String, db.ForeignKey("department.dept_code"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


class Faculty(db.Model):
    __tablename__ = 'faculty'
    f_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String)
    gender = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    dept_code = db.Column(db.String, db.ForeignKey("department.dept_code"), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


class Member(db.Model):
    __tablename__ = 'member'
    m_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    roll = db.Column(db.String, db.ForeignKey("student.roll"))
    f_id = db.Column(db.String, db.ForeignKey("faculty.f_id"))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    max_issue_left = db.Column(db.Integer, nullable=False)
    fine = db.Column(db.Integer, nullable=False)
    

class Department(db.Model):
    __tablename__ = 'department'
    dept_code = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    building = db.Column(db.String, nullable=False)


class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    f_author = db.Column(db.String, nullable=False)
    s_author = db.Column(db.String)
    t_author = db.Column(db.String)
    copies = db.Column(db.Integer, nullable=False)


class B_Copies(db.Model):
    __tablename__ = 'book_copies'
    b_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    isbn = db.Column(db.String, db.ForeignKey("book.isbn"), nullable=False)
    assigned = db.Column(db.String, nullable=False)


class B_Issue(db.Model):
    __tablename__ = 'book_issue'
    m_id = db.Column(db.String, db.ForeignKey("member.m_id"), primary_key=True, nullable=False)
    b_id = db.Column(db.String, db.ForeignKey("book_copies.b_id"), primary_key=True, nullable=False)
    doi = db.Column(db.String, nullable=False)
    dor = db.Column(db.String, nullable=False)



