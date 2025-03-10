from flask import render_template, request, redirect, url_for, flash
from models import BlogPost, db

def register_routes(app):
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
