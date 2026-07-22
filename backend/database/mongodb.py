from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure

# Create MongoDB object
mongo = PyMongo()


def init_db(app):
    """
    Initialize MongoDB with Flask app.
    """
    mongo.init_app(app)

    try:
        # Check MongoDB connection
        mongo.cx.admin.command("ping")
        print("=" * 60)
        print("✅ MongoDB Connected Successfully")
        print("=" * 60)

    except ConnectionFailure:
        print("=" * 60)
        print("❌ MongoDB Connection Failed")
        print("=" * 60)


# ==============================
# Collections
# ==============================

def users_collection():
    return mongo.db.users


def students_collection():
    return mongo.db.students


def faculty_collection():
    return mongo.db.faculty


def admins_collection():
    return mongo.db.admins


def exams_collection():
    return mongo.db.exams


def question_papers_collection():
    return mongo.db.question_papers


def questions_collection():
    return mongo.db.questions


def answer_keys_collection():
    return mongo.db.answer_keys


def subjects_collection():
    return mongo.db.subjects


def answer_scripts_collection():
    return mongo.db.answer_scripts


def evaluations_collection():
    return mongo.db.evaluations


def reports_collection():
    return mongo.db.reports


def analytics_collection():
    return mongo.db.analytics


def notifications_collection():
    return mongo.db.notifications


def logs_collection():
    return mongo.db.logs
