from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('neet.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        chapter TEXT,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subjects')
def subjects():
    return render_template('subjects.html')

@app.route('/chapters/<subject>')
def chapters(subject):
    conn = sqlite3.connect('neet.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT chapter FROM questions WHERE subject=?", (subject,))
    chapters = c.fetchall()
    conn.close()
    return render_template('chapters.html', subject=subject, chapters=chapters)

@app.route('/quiz/<subject>/<chapter>', methods=['GET', 'POST'])
def quiz(subject, chapter):
    conn = sqlite3.connect('neet.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE subject=? AND chapter=?", (subject, chapter))
    questions = c.fetchall()
    conn.close()

    q_index = int(request.args.get('q', 0))
    score = int(request.args.get('score', 0))

    if request.method == 'POST':
        selected = request.form.get('answer')
        correct = questions[q_index][8]

        if selected == correct:
            score += 4
        else:
            score -= 1

        q_index += 1

    if q_index >= len(questions):
        return render_template('result.html', score=score)

    return render_template('quiz.html',
                           q=questions[q_index],
                           q_index=q_index,
                           score=score)

if __name__ == '__main__':
    app.run()
