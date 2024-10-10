from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
import os

app = Flask(__name__)
app.secret_key = '12345678'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import BlogPost

# Create the database within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).limit(5).all()
    return render_template('index.html', posts=posts)

@app.route('/admin/dashboard')
def admin_dashboard():
    posts = BlogPost.query.all()
    return render_template('admin/dashboard.html', posts=posts)

@app.route('/admin/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = BlogPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/create_post.html')

@app.route('/admin/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit_post.html', post=post)

@app.route('/admin/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/blog/<int:post_id>')
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
