from flask_pymongo import PyMongo

mongo = PyMongo()


def init_db(app):
    """Attach MongoDB to the Flask application.

    PyMongo connects lazily.  Avoid a synchronous ping here because it can
    prevent the API from starting for the server-selection timeout when Mongo
    is temporarily unavailable.
    """
    mongo.init_app(app)


# Compatibility for the newer controllers that use ``db.collection``.
db = mongo.db


def users_collection(): return mongo.db.users
def students_collection(): return mongo.db.students
def faculty_collection(): return mongo.db.faculty
def admins_collection(): return mongo.db.admins
def exams_collection(): return mongo.db.exams
def question_papers_collection(): return mongo.db.question_papers
def questions_collection(): return mongo.db.questions
def answer_keys_collection(): return mongo.db.answer_keys
def subjects_collection(): return mongo.db.subjects
def answer_scripts_collection(): return mongo.db.answer_scripts
def evaluations_collection(): return mongo.db.evaluations
def reports_collection(): return mongo.db.reports
def analytics_collection(): return mongo.db.analytics
def notifications_collection(): return mongo.db.notifications
def logs_collection(): return mongo.db.logs


def ensure_evaluation_indexes():
    """Create lookup indexes when evaluation persistence is first used.

    This is intentionally not called during Flask startup, preserving lazy
    database behaviour when MongoDB is temporarily unavailable.
    """
    mongo.db.evaluations.create_index("answerSheetId", unique=True, sparse=True)
    mongo.db.evaluations.create_index([("studentEmail", 1), ("createdAt", -1)])
    mongo.db.evaluations.create_index([("examId", 1), ("studentEmail", 1)])
    mongo.db.answer_scripts.create_index([("examId", 1), ("studentEmail", 1)])
    mongo.db.questions.create_index([("examId", 1), ("questionNumber", 1)])
    mongo.db.answer_keys.create_index([("examId", 1), ("questionNumber", 1)])
