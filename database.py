import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("password"),
    database="student_management"
)
mycursor = mydb.cursor()

'''
mycursor.execute("SHOW TABLES")
for table in mycursor:
    print(table)
'''

# Create tables if they do not exist already
def createTables():
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            studentID INT AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(255), 
            email VARCHAR(255)
        )
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            courseID INT AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(255), 
            description VARCHAR(255)
        )
    """)
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollment (
            enrollmentID INT AUTO_INCREMENT PRIMARY KEY, 
            studentID INT, 
            courseID INT, 
            FOREIGN KEY (studentID) REFERENCES students(studentID), 
            FOREIGN KEY (courseID) REFERENCES courses(courseID)
        )
    """)

createTables()

def main():
    while True:
        print("Menu")
        print("1: View students")
        print("2: View courses")
        print("3: Add student")
        print("4: Add course")
        print("5: Enroll student in a course")
        print("6: Exit")
        action = int(input("Enter action (1-6): "))      
        print("")

        if(action == 3):
            print("Enter student details:")
            name = input("Enter student: ")
            email = input("Enter email: ")
            mycursor.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
            mydb.commit()
            print("Student successfully added")
        
        if(action == 4):
            print("Enter course details:")
            name = input("Enter course: ")
            description = input("Enter course description: ")
            mycursor.execute("INSERT INTO courses (name, description) VALUES (%s, %s)", (name, description))
            mydb.commit()
            print("Course successfully added")

        if(action == 5):
            # Select student and course
            print("List of students: ")
            mycursor.execute("SELECT * FROM students")
            for student in mycursor:
                print(f"{student[0]}: {student[1]}")
            studentID = input("Select a student (enter id): ")
            print()
            print("List of courses: ")
            mycursor.execute("SELECT * FROM courses")
            for course in mycursor:
                print(f"{course[0]}: {course[1]}")
            courseID = input("Select a course to enroll in (enter id): ")

            # Add enrollment
            mycursor.execute("INSERT INTO enrollment (studentID, courseID) VALUES (%s, %s)", (studentID, courseID))
            mydb.commit()
            print("Student succesfully enrolled")

        elif (action == 6):
            break

        print("")

main()
mydb.commit()