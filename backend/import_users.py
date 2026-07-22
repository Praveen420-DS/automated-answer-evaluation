"""Import the supplied student, staff, and admin CSV files into MongoDB.

Run from the backend directory:
    python import_users.py

The command is safe to run more than once.  Users are matched by email and
updated in place, while passwords are only set on the first import so local
password changes are not overwritten.
"""

import csv
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient, UpdateOne
from werkzeug.security import generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def csv_rows(filename):
    """Return CSV rows with whitespace-only values normalised to empty text."""
    with (DATA_DIR / filename).open(encoding="utf-8-sig", newline="") as file:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(file)
        ]


def user_from_student(row):
    return {
        "fullName": row["Name"], "email": row["Email"].lower(), "role": "student",
        "studentId": row["Student ID"], "department": row["Department"],
        "year": int(row["Year"]), "section": row["Section"],
        "rollNo": row["Roll No"], "status": row["Status"],
    }


def user_from_staff(row):
    return {
        "fullName": row["Name"], "email": row["Email"].lower(), "role": "faculty",
        "facultyId": row["Teacher ID"], "department": row["Department"],
        "designation": row["Designation"], "subject": row["Subject"],
        "status": row["Status"],
    }


def user_from_admin(row):
    return {
        "fullName": row["Name"], "email": row["Email"].lower(), "role": "admin",
        "adminId": row["Admin ID"], "adminRole": row.get("Role", ""),
        "status": row["Status"],
    }


def import_group(users, filename, factory):
    operations = []
    now = datetime.now(timezone.utc)
    for row in csv_rows(filename):
        document = factory(row)
        password = row["Password"]
        # $setOnInsert prevents a re-import from unexpectedly resetting passwords.
        operations.append(UpdateOne(
            {"email": document["email"]},
            {"$set": {**document, "updatedAt": now},
             "$setOnInsert": {"password": generate_password_hash(password), "createdAt": now}},
            upsert=True,
        ))

    result = users.bulk_write(operations, ordered=False)
    return len(operations), result.upserted_count, result.modified_count


def main():
    load_dotenv(BASE_DIR / ".env")
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/evalai")

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    try:
        client.admin.command("ping")
        # Flask-PyMongo uses the database embedded in MONGO_URI, so use that
        # same database instead of the legacy MONGO_DB setting.
        database = client.get_default_database()
        users = database.users
        users.create_index([("email", ASCENDING)], unique=True)

        groups = (
            ("students", "Automated_Answer_Evaluation_Login_Data-Students.csv", user_from_student),
            ("staff", "Automated_Answer_Evaluation_Login_Data-Teachers.csv", user_from_staff),
            ("admins", "Automated_Answer_Evaluation_Login_Data-Admin.csv", user_from_admin),
        )
        for label, filename, factory in groups:
            total, inserted, updated = import_group(users, filename, factory)
            print(f"{label.title()}: {total} processed ({inserted} inserted, {updated} updated)")
        print(f"Complete. Users are stored in '{database.name}.users'.")
    finally:
        client.close()


if __name__ == "__main__":
    main()
