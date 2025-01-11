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
mycursor.execute("SHOW TABLES")
for table in mycursor:
    print(table)

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

