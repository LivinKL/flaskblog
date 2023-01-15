import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def connect_db():
	conn=sqlite3.connect('database.db')
	conn.row_factory=sqlite3.Row
	return conn
	
def get_post(post_id):
	conn=connect_db()
	post=conn.execute('SELECT * FROM blog where id = ?',(post_id,)).fetchone()
	conn.close()
	if post is None:
		abort(404)
	return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your key bleh'


@app.route('/')
def index():
    conn = connect_db()
    posts = conn.execute('SELECT * FROM blog').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
	post=get_post(post_id)
	return render_template('show_post.html', post=post)
	
@app.route('/team')
def show_team():
	return render_template('team.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
	        title = request.form['title']
	        content = request.form['content']
	        author = request.form['author']

	        if not title:
	            flash('Title is required!')
	        else:
	            conn = connect_db()
	            conn.execute('INSERT INTO blog (title, content, author) VALUES (?, ?, ?)',
                         (title, content, author))
	            conn.commit()
	            conn.close()
	            return redirect(url_for('index'))
	return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
	post = get_post(id)

	if request.method == 'POST':
	        title = request.form['title']
	        content = request.form['content']
	        author = request.form['author']

	        if not title:
	            flash('Title is required!')
	        else:
	            conn = connect_db()
	            conn.execute('UPDATE blog SET title = ?, content = ?, author=?'
                         ' WHERE id = ?',
                         (title, content, author, id))
	            conn.commit()
	            conn.close()
	            return redirect(url_for('index'))

	return render_template('edit.html', post=post)	



@app.route('/<int:id>/delete')
def delete(id):
	post = get_post(id)
	conn = connect_db()
	conn.execute('DELETE FROM blog WHERE id = ?', (id,))
	conn.commit()
	conn.close()
	flash('"{}" was successfully deleted!'.format(post['title']))
	return redirect(url_for('index'))	
