import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("password"),
    database="student_management"
)
print(conn)