from app import app, AdminUser
from werkzeug.security import check_password_hash

username = "admin"  # Replace with the username you want to check
input_password = "your_secure_password"  # Replace with the password you want to verify

# Create an application context
with app.app_context():
    user = AdminUser.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, input_password):
            print("Password is correct.")
        else:
            print("Password is incorrect.")
    else:
        print("User not found.")
