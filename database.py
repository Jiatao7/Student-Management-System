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

def printMenu():
    print("Menu")
    print("1: View students")
    print("2: View courses")
    print("3: Add student")
    print("4: Add course")
    print("5: Enroll student in a course")
    print("6: Exit")

def viewStudents():
    print("All students")
    mycursor.execute("SELECT * FROM students")
    for student in mycursor:
        print(f"{student[1]}: {student[2]} | ID: {student[0]}")
    while True:
        action = input("Enter a student's id to view more details (or press enter to exit): ")
        if(action):
            studentID = int(action)
            mycursor.execute(f"SELECT * FROM students WHERE studentID = {studentID}")
            student = mycursor.fetchone()
            print()
            print(student[1])
            print(f"Email: {student[2]}")

            # Find all courses the student is taking
            courseList = []
            mycursor.execute(f"""SELECT courses.name FROM courses
                INNER JOIN enrollment
                USING(courseID)
                WHERE studentID = {studentID};
            """)
            courses = mycursor.fetchall()
            for course in courses:
                courseList.append(course[0])
            print("Courses: " + ", ".join(courseList))

            input("Press enter to exit: ")
            print()
        else:
            break

def viewCourses():
    print("All courses")
    mycursor.execute("SELECT * FROM courses")
    for course in mycursor:
        print(f"{course[1]}: {course[2]} | ID: {course[0]}")
    while True:
        action = input("Enter a course's id to view more details (or press enter to exit): ")
        if(action):
            courseID = int(action)
            mycursor.execute(f"SELECT * FROM courses WHERE courseID = {courseID}")
            course = mycursor.fetchone()
            print()
            print(course[1])
            print(f"Description: {course[2]}")

            # Find all students in course
            studentList = []
            mycursor.execute(f"""SELECT students.name FROM students
                INNER JOIN enrollment
                USING(studentID)
                WHERE courseID = {courseID};
            """)
            students = mycursor.fetchall()
            for student in students:
                studentList.append(student[0])
            print("Students Enrolled: " + ", ".join(studentList))

            input("Press enter to exit: ")
            print()
        else:
            break

def addStudent():
    print("Enter student details:")
    name = input("Enter student: ")
    email = input("Enter email: ")
    mycursor.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
    mydb.commit()
    print("Student successfully added")

def addCourse():
    print("Enter course details:")
    name = input("Enter course name: ")
    description = input("Enter course description: ")
    mycursor.execute("INSERT INTO courses (name, description) VALUES (%s, %s)", (name, description))
    mydb.commit()
    print("Course successfully added")

def enroll():
    # Select student and course
    print("List of students: ")
    mycursor.execute("SELECT * FROM students")
    for student in mycursor:
        print(f"{student[1]} - {student[0]}")
    studentID = input("Select a student (enter id): ")
    print()
    print("List of courses: ")
    mycursor.execute("SELECT * FROM courses")
    for course in mycursor:
        print(f"{course[1]} - {course[0]}")
    courseID = input("Select a course to enroll in (enter id): ")

    # Add enrollment
    mycursor.execute("INSERT INTO enrollment (studentID, courseID) VALUES (%s, %s)", (studentID, courseID))
    mydb.commit()
    print("Student successfully enrolled")

def main():
    createTables()

    while True:
        printMenu()
        action = int(input("Enter action (1-6): "))      
        print("")
        if(action == 1):
            viewStudents()
        elif(action == 2):
            viewCourses()
        elif(action == 3):
            addStudent()
        elif(action == 4):
            addCourse()
        elif(action == 5):
            enroll()
        elif (action == 6):
            break
        print("")

# Run program
if __name__ == "__main__":
    main()

# Close connection
mydb.close()