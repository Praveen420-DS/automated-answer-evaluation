import sqlite3

# Connect to the database
conn = sqlite3.connect("answer_evaluation.db")
cursor = conn.cursor()

# Insert sample data
cursor.execute("""
INSERT INTO evaluations
(question, model_answer, student_answer, marks, grade, feedback)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    "What is AI?",
    "Artificial Intelligence is the simulation of human intelligence by machines.",
    "AI is making computers think like humans.",
    8.5,
    "A",
    "Good answer. Covers the main concept."
))

# Save changes
conn.commit()

# Display all records
cursor.execute("SELECT * FROM evaluations")

rows = cursor.fetchall()

print("\nStored Records:\n")

for row in rows:
    print(row)

# Close connection
conn.close()