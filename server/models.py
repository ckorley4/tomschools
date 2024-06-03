from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db
from datetime import datetime
from flask_httpauth import HTTPTokenAuth

# Models go here!
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


# Models go here!
   

class Student(db.Model,SerializerMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer,primary_key=True)
    program = db.Column(db.String)
    name = db.Column(db.String)
    year_of_birth = db.Column(db.Integer)
    photo = db.Column(db.LargeBinary)
    course = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #enrollments = db.relationship('Enrollment',back_populates='student',cascade="all,delete")
    
   

    def __repr__(self):
        return f'<Student {self.id}: {self.name}>'

class Enrollment(db.Model,SerializerMixin):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    #student = db.relationship('Student',back_populates='enrollments',cascade="all,delete")
    #course =  db.relationship('Course',back_populates='enrollments',cascade="all,delete")
    user_id = db.Column(db.Integer)
    #user = db.relationship("Users", back_populates="enrollment")
    #serialize_rules = ( "-student.enrollments","-course.enrollments" )

    def __repr__(self):
        return f'<Enrollment {self.id} >'

class Molas(db.Model,SerializerMixin):
    __tablename__='me'
    id = db.Column(db.Integer, primary_key=True)
    student_id= db.Column(db.Integer)
    course_id= db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
class Course(db.Model,SerializerMixin):
    __tablename__ = 'courses'

    id = db.Column(db.Integer,primary_key= True)
    description = db.Column(db.String)
    category = db.Column(db.String)
    image = db.Column(db.String)
    title = db.Column(db.String)
    venue_id = db.Column(db.String,db.ForeignKey('venues.id'))
    instructor_id = db.Column(db.Integer,db.ForeignKey('instructors.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    instructor = db.relationship('Instructor',back_populates='courses',cascade="all,delete")
    venue = db.relationship('Venue',back_populates='courses',cascade="all,delete")
    #enrollments = db.relationship('Enrollment',back_populates='course',cascade="all,delete")
    serialize_rules = ("-instructor.courses","-venue.courses")

    def __repr__(self):
        return f'<Course {self.id}  {self.description}>'

class Instructor(db.Model,SerializerMixin):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    department = db.Column(db.String)
    specialty = db.Column(db.String)
    courses=db.relationship(Course,back_populates='instructor')



    def __repr__(self):
        return f'<Instructor {self.id}  {self.name}>'

class Venue(db.Model,SerializerMixin):
    __tablename__ = 'venues'
    
    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String)
    courses=db.relationship(Course,back_populates='venue')

    def __repr__(self):
        return f'<Venue {self.id}  {self.location}>'
    
class Users(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email =db.Column(db.String(255), nullable=False, unique=True)
    username =db.Column(db.String(100), nullable=False, unique=True)
   

    #enrollment = db.relationship("Enrollment", back_populates="user")

    serialize_rules = ('-password_hash',)  # Example rule to exclude password_hash from serialization

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"


class User(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(250))

    
    