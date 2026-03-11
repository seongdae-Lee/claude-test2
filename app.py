from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_wtf.csrf import CSRFProtect
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DB_PATH = os.path.join(os.path.dirname(__file__), 'board.db')

csrf = CSRFProtect(app)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    # g 객체 없이 직접 커넥션 생성 (앱 컨텍스트 외부에서도 호출 가능)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    posts = get_db().execute(
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
            db = get_db()
            db.execute(
                'INSERT INTO posts (title, author, content) VALUES (?, ?, ?)',
                (title, author, content)
            )
            db.commit()
            return redirect(url_for('index'))
        flash('제목, 작성자, 내용을 모두 입력해주세요.')
        return render_template('write.html')
    return render_template('write.html')


@app.route('/post/<int:post_id>')
def view(post_id):
    post = get_db().execute(
        'SELECT * FROM posts WHERE id = ?', (post_id,)
    ).fetchone()
    if post is None:
        return redirect(url_for('index'))
    return render_template('view.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    return redirect(url_for('index'))


init_db()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true', port=5000)
