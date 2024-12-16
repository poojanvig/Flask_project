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

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


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


@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Create a new contact instance
        new_contact = Contact(name=name, email=email, phone=phone, message=message)

        # Add to the session and commit to save in the database
        db.session.add(new_contact)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('index'))


@app.route('/stay-updated', methods=['POST'])
def stay_updated():
    if request.method == 'POST':
        email = request.form.get('email')

        # Create a new subscription instance
        new_subscription = Subscription(email=email)

        # Add to the session and commit to save in the database
        db.session.add(new_subscription)
        db.session.commit()

        flash('Thank you for subscribing!', 'success')
        return redirect(url_for('index'))


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




@app.route('/admin')
@login_required
def admin_dashboard():
    posts = BlogPost.query.all()
    contacts = Contact.query.order_by(Contact.date_submitted.desc()).all()  # Get all contact submissions
    subscriptions = Subscription.query.order_by(Subscription.date_submitted.desc()).all()  # Get all subscriptions
    return render_template('admin/dashboard.html', posts=posts, contacts=contacts, subscriptions=subscriptions)


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

@app.route('/project/Sumitra')
def Sumitra_project():
    return render_template('projects/Sumitra.html')

@app.route('/project/trinity')
def trinity_project():
    return render_template('projects/trinity.html')

if __name__ == '__main__':
    app.run(debug=True)