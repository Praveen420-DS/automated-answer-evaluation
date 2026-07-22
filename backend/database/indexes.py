def create_indexes(db):
    db.users.create_index('email', unique=True)
    db.exams.create_index('faculty_id')
