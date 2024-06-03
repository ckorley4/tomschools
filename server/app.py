#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, request, make_response
from flask_restful import Resource,Api
from flask import Flask, make_response, jsonify,session,redirect,url_for
from authlib.integrations.flask_client import OAuth
import os,ipdb
from flask_migrate import Migrate
# Local imports
from config import app,db
from models import Venue,Student,Instructor,Course,Enrollment,Users,User,Molas
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash



@app.route('/students', methods=['GET'])
def index():
    student_list =[student.to_dict() for student in Student.query.all()]
    return make_response(student_list,200)

@app.route('/students/<int:id>', methods =['GET','PATCH','DELETE'])
def student_by_id(id):
    student = Student.query.filter(Student.id == id).first()
    if student:
        if request.method == 'DELETE':
            db.session.delete(student)
            db.session.commit()
            return make_response(student.to_dict(),202)
        elif request.method == 'GET':
            return make_response(student.to_dict(rules=("-enrollments",)),200)
        elif request.method == 'PATCH':
            try:
                incoming = request.get_json()
                for attr in incoming:
                    setattr(student,attr,incoming[attr])
                    db.session.commit()
                return make_response(student.to_dict(),201)
            except:
                return make_response({"errors": ["validation errors"]},400)
        else:
            return make_response({"error": "Student not Found"},404)

@app.route('/enrollments/student/<int:id>')
def enrollment_student_by_id(id):
   student_enroll_list= Enrollment.query.filter(Enrollment.student_id==id).all()
   enrollment_student = [enrollment.to_dict() for enrollment in student_enroll_list]
   if enrollment_student:
        return make_response(enrollment_student,200)
   else:
        return make_response({"Error":"NO enrollments found"},404)
        
@app.route('/enrollments/<int:id>', methods =['GET','PATCH','DELETE'])
def enrollment_by_id(id):
    enrollment = Enrollment.query.filter(Enrollment.id == id).first()
    if enrollment:
        if request.method == 'DELETE':
            db.session.delete(enrollment)
            db.session.commit()
            return make_response(enrollment.to_dict(),202)
        elif request.method == 'PATCH':
            try:
                incoming = request.get_json()
                for attr in incoming:
                    setattr(enrollment,attr,incoming[attr])
                    db.session.commit()
                return make_response(enrollment.to_dict(),201)
            except:
                return make_response({"errors": ["validation errors"]},400)
        elif request.method == 'GET':
             return make_response(enrollment.to_dict(),200)
        else:
            return make_response({"error": "Enroolment not Found"},404)
   
        


@app.route('/courses/<int:id>', methods =['GET','PATCH','DELETE'])
def course_by_id(id):
    course = Course.query.filter(Course.id == id).first()
    if course:
        if request.method == 'DELETE':
            db.session.delete(course)
            db.session.commit()
            return make_response(course.to_dict(),202)
        elif request.method == 'GET':
            return make_response(course.to_dict(rules=("-enrollments",)),200)
        elif request.method == 'PATCH':
            try:
                incoming = request.get_json()
                for attr in incoming:
                    setattr(course,attr,incoming[attr])
                    db.session.commit()
                return make_response(course.to_dict(),201)
            except:
                return make_response({"errors": ["validation errors"]},400)
            
        else:
            return make_response({"error": "Student not Found"},404)
@app.route('/students',methods =['POST'])
def new():
     try:
        incoming = request.get_json()
        new_student = Student(**incoming)
        db.session.add(new_student)
        db.session.commit()
        return make_response(new_student.to_dict,201)
     except:
        return make_response({"errors": ["Nii"]},400)
     else:
         return make_response({"error": "Student not Found"},404)
   

@app.route('/venues', methods=['GET'])
def venues():
    venue_list =[venue.to_dict() for venue in Venue.query.all()]
    return make_response(venue_list,200)

@app.route('/instructors', methods=['GET'])
def instructors():
    instructor_list =[instructor.to_dict() for instructor in Instructor.query.all()]
    return make_response(instructor_list,200)


@app.route('/courses', methods=['GET'])
def courses():
    email = dict(session).get('email',None)
    course_list =[course.to_dict() for course in Course.query.all()]
    return make_response(course_list,200)

@app.route('/enrollments', methods=['GET','POST'])
def enrollments():
     if request.method == "GET":
        enrollment_list =[enrollment.to_dict() for enrollment in Enrollment.query.all()]
        return make_response(enrollment_list,200)
     elif request.method == "POST":
        #ipdb.set_trace()
        incoming = request.get_json()
        student_id =incoming['student_id']
        #user_id=incoming['user_id']
        course_id=incoming['course_id']
        new = Enrollment(**incoming)
        db.session.add(new)
        db.session.commit()
        return make_response(new.to_dict(),201)

@app.route('/users', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Check if user already exists
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists'}), 400

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create and add new user to database
    new_user = Users(email=email, username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Return user_id and username along with success message
    return jsonify({
        'message': 'User registered successfully',
        'user_id': new_user.id,
        'username': new_user.username
    }), 201

# Log in an existing user

tokens = {}

@app.route('/auth/google', methods=['POST'])
def google_login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        user = User(name=data['name'], email=data['email'], provider='google', image_url=data['imageUrl'])
        db.session.add(user)
        db.session.commit()
    
    token = os.urandom(24).hex()
    tokens[token] = user.email
    response = make_response(jsonify({'message': 'Login successful'}))
    response.set_cookie('token', token)
    return response




#New things start here
users = {}

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email in users:
        return jsonify({'error': 'User already exists'}), 400

    users[email] = password
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email not in users or users[email] != password:
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'message': 'Sign in successful'}), 200

GITHUB_CLIENT_ID = 'Ov23liI8zvyd2KimM2IE'
GITHUB_CLIENT_SECRET = 'b8109b35a3adca5ddc3fcfaeb86edc5ac210e393'

@app.route('/github/login', methods=['POST'])
def github_login():
    code = request.json.get('code')
    if not code:
        return jsonify({'error': 'Code is required'}), 400

    # Exchange code for access token
    token_response = requests.post(
        'https://github.com/login/oauth/access_token',
        headers={'Accept': 'application/json'},
        data={
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': code
        }
    )

    token_json = token_response.json()
    access_token = token_json.get('access_token')
    if not access_token:
        return jsonify({'error': 'Failed to get access token'}), 400

    # Get user info
    user_response = requests.get(
        'https://api.github.com/user',
        headers={
            'Authorization': f'token {access_token}',
            'Accept': 'application/json'
        }
    )
    user_json = user_response.json()
    return jsonify(user_json)

if __name__ == '__main__':
    app.run(port=5555, debug=True)


