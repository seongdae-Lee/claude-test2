from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'board.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')


@app.route('/')
def index():
    with get_db() as conn:
        posts = conn.execute(
            'SELECT id, title, author, created_at FROM posts ORDER BY id DESC'
        ).fetchall()
    return render_template('index.html', posts=posts)


@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        content = request.form['content'].strip()
        if title and author and content:
            with get_db() as conn:
                conn.execute(
                    'INSERT INTO posts (title, author, content) VALUES (?, ?, ?)',
                    (title, author, content)
                )
        return redirect(url_for('index'))
    return render_template('write.html')


@app.route('/post/<int:post_id>')
def view(post_id):
    with get_db() as conn:
        post = conn.execute(
            'SELECT * FROM posts WHERE id = ?', (post_id,)
        ).fetchone()
    if post is None:
        return redirect(url_for('index'))
    return render_template('view.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with get_db() as conn:
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    return redirect(url_for('index'))


init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
