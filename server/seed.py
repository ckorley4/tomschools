#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Student, Venue, Course, Instructor, Enrollment

if __name__ == '__main__':
    fake = Faker()
    
    with app.app_context():
        print("Starting seed...")
        
        # Deleting existing data
        print("Deleting students...")
        Student.query.delete()
        
        print("Deleting instructors...")
        Instructor.query.delete()
        
        print("Deleting venues...")
        Venue.query.delete()
        
        print("Deleting courses...")
        Course.query.delete()
        
        print("Deleting enrollments...")
        Enrollment.query.delete()
        
        # Creating Students
        print("Creating Students")
        students = []
        for i in range(1, 16):
            student = Student(
                program=fake.job(),
                year_of_birth=fake.year(),
                name=fake.name(),
                course=randint(1, 5)
            )
            students.append(student)
        
        db.session.add_all(students)
        db.session.commit()

        # Creating Venues
        print("Creating Venues")
        venues = []
        for location in ["Ga Mashie", "Awoshie", "Bukom", "Ashongman", "Kaneshie"]:
            venue = Venue(location=location)
            venues.append(venue)
        
        db.session.add_all(venues)
        db.session.commit()
        
        # Creating Instructors
        print("Creating Instructors")
        instructors = []
        for i in range(1, 5):
            instructor = Instructor(
                name=fake.name(),
                specialty=fake.job(),
                department=fake.company()
            )
            instructors.append(instructor)
        
        db.session.add_all(instructors)
        db.session.commit()
        
        # Creating Courses with tech-related names, images, and descriptions
        print("Creating Courses")
        tech_images = [
            "https://example.com/tech_image1.jpg",
            "https://example.com/tech_image2.jpg",
            "https://example.com/tech_image3.jpg",
            # Add more tech-related image URLs here
        ]
        
        course_titles = [
            "Introduction to Python Programming",
            "Advanced JavaScript",
            "Machine Learning with Python",
            "Data Structures and Algorithms",
            "Introduction to Cloud Computing",
            "Full-Stack Web Development",
            "DevOps Essentials",
            "Cyber Security Basics",
            "Mobile App Development",
            "Artificial Intelligence",
            # Add more course titles here
        ]

        courses = []
        for _ in range(100):
            course = Course(
                title=rc(course_titles),
                category="Technology",
                image=rc(tech_images),
                instructor_id=randint(1, 4),
                venue_id=randint(1, 5),
                description=fake.paragraph(nb_sentences=5)
            )
            courses.append(course)
        
        db.session.add_all(courses)
        db.session.commit()

        # Creating Enrollments
        print("Creating Enrollments")
        enrollments = []
        for _ in range(50):  # assuming 50 enrollments for example
            enrollment = Enrollment(
                student_id=randint(1, 15),
                course_id=randint(1, 100),
                user_id=randint(1, 4)  # assuming 4 users
            )
            enrollments.append(enrollment)
        
        db.session.add_all(enrollments)
        db.session.commit()

        print("Seeding completed!")
