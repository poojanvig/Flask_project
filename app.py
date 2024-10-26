from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # Set this to a unique key
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
login_manager = LoginManager(app)  # Initialize Flask-Login
login_manager.login_view = 'login'  # Specify the login route

# Database model for BlogPost
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(120), nullable=True)  # For blog images

# Database model for Admin User
class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

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

# Route for admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AdminUser.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('admin/login.html')

# Route for admin logout
@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))




# Route for admin dashboard to create, edit, and delete posts
@app.route('/admin')
@login_required
def admin_dashboard():
    posts = BlogPost.query.all()
    return render_template('admin/dashboard.html', posts=posts)




@app.route('/admin/create', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/saburi_apartments')
def sumitra_apartments():
    return render_template('projects/saburi.html')

# Routes for project pages
@app.route('/project/saburi')
def saburi_project():
    return render_template('projects/saburi.html')

@app.route('/project/maha_kunj')
def maha_kunj_project():
    return render_template('projects/maha_kunj.html')

@app.route('/project/maha_res')
def maha_res_project():
    return render_template('projects/maha_res.html')

if __name__ == '__main__':
    app.run(debug=True)