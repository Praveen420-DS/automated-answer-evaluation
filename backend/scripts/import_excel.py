import pandas as pd
from pymongo import MongoClient

# Replace with your MongoDB URI
client = MongoClient("YOUR_MONGODB_URI")

db = client["answer_evaluation"]

excel_file = "../data/Automated_Answer_Evaluation_Login_Data.xlsx"

# ---------------- Students ----------------
students = pd.read_excel(excel_file, sheet_name="Students")

student_docs = []

for _, row in students.iterrows():
    student_docs.append({
        "student_id": row["Student ID"],
        "name": row["Name"],
        "email": row["Email"],
        "password": row["Password"],
        "department": row["Department"],
        "year": row["Year"],
        "section": row["Section"],
        "roll_no": row["Roll No"],
        "role": "student",
        "status": row["Status"]
    })

db.students.insert_many(student_docs)

# ---------------- Faculty ----------------
teachers = pd.read_excel(excel_file, sheet_name="Teachers")

teacher_docs = []

for _, row in teachers.iterrows():
    teacher_docs.append({
        "faculty_id": row["Teacher ID"],
        "name": row["Name"],
        "email": row["Email"],
        "password": row["Password"],
        "department": row["Department"],
        "designation": row["Designation"],
        "subject": row["Subject"],
        "role": "faculty",
        "status": row["Status"]
    })

db.faculty.insert_many(teacher_docs)

# ---------------- Admin ----------------
admins = pd.read_excel(excel_file, sheet_name="Admin")

admin_docs = []

for _, row in admins.iterrows():
    admin_docs.append({
        "admin_id": row["Admin ID"],
        "name": row["Name"],
        "email": row["Email"],
        "password": row["Password"],
        "role": "admin",
        "status": row["Status"]
    })

db.admins.insert_many(admin_docs)

print("Excel imported successfully!")