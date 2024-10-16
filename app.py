from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # Set this to a unique key
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Database model for BlogPost
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(120), nullable=True)  # For blog images

# Initialize the database
with app.app_context():
    db.create_all()

# Route for homepage that displays blog posts
@app.route('/')
def index():
    blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).limit(5).all()
    return render_template('index.html', blog_posts=blog_posts)

# Route for viewing an individual blog post
@app.route('/blog/<int:blog_id>')
def view_blog(blog_id):
    post = BlogPost.query.get_or_404(blog_id)
    return render_template('view_blog.html', post=post)

# Route for admin dashboard to create, edit, and delete posts
@app.route('/admin/dashboard')
def admin_dashboard():
    posts = BlogPost.query.all()
    return render_template('admin/dashboard.html', posts=posts)

@app.route('/admin/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files.get('image')
        image_filename = None
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join('static/uploads', image_filename))
        new_post = BlogPost(title=title, content=content, image=image_filename)
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
        image = request.files.get('image')
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join('static/uploads', image_filename))
            post.image = image_filename
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

# Routes for project pages
@app.route('/project/saburi')
def saburi_project():
    return render_template('saburi.html')

@app.route('/project/maha_kunj')
def maha_kunj_project():
    return render_template('maha_kunj.html')

@app.route('/project/maha_res')
def maha_res_project():
    return render_template('maha_res.html')

if __name__ == '__main__':
    app.run(debug=True)