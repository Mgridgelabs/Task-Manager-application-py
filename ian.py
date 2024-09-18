# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import User

# # Setup
# engine = create_engine('sqlite:///path/to/your/database.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# # Add User
# new_user = User(name="Test User", email="test@example.com", password="password")
# session.add(new_user)
# session.commit()

# # Check if user exists
# user = session.query(User).filter_by(email="test@example.com").first()
# if user:
#     print(f"User found: {user.name}")
# else:
#     print("User not found.")

# from models import User, engine
# from sqlalchemy.orm import sessionmaker
# from werkzeug.security import generate_password_hash, check_password_hash

# Session = sessionmaker(bind=engine)
# session = Session()

# # Test user credentials
# test_email = 'maina@gmail.com'
# test_password = 'your_password'

# # Fetch the user
# user = session.query(User).filter_by(email=test_email).first()

# if user:
#     print(f"Stored password hash: {user.password}")
#     # Verify password
#     if user.check_password(test_password):
#         print("Password is correct!")
#     else:
#         print("Password is incorrect.")
# else:
#     print("User not found.")

# # Update the password for the user
# user.password = generate_password_hash('new_password')
# session.commit()

# print(f"Updated password for {user.email}")

from models import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Specify the email of the user you want to delete
user_email = 'maina@gmail.com'

# Fetch the user
user = session.query(User).filter_by(email=user_email).first()

if user:
    print(f"User found: {user.name}")
    # Delete the user from the session
    session.delete(user)
    session.commit()
    print(f"User {user.name} has been deleted.")
else:
    print("User not found.")

