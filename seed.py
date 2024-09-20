from models import User, Task, Category, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Set up database session
Session = sessionmaker(bind=engine)
session = Session()

def seed():
    # Create default categories
    categories = ['Work', 'Personal', 'Health', 'Finance']
    category_objects = []
    for category_name in categories:
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            session.add(category)
            session.commit()  # Commit to assign an ID
        category_objects.append(category)
    
    # Create a default user (for testing/demo purposes)
    default_user_email = "demo@demo.com"
    default_user = session.query(User).filter_by(email=default_user_email).first()
    if not default_user:
        demo_user = User(name="Demo User", email=default_user_email)
        demo_user.set_password("password")  # Hash the password
        session.add(demo_user)
        session.commit()
        default_user = demo_user  # Update default_user to reference demo_user
        print(f"Created user: {default_user.name} with email: {default_user.email}")
    else:
        print(f"User already exists: {default_user.name} with email: {default_user.email}")
    
    # Create some tasks for the demo user
    existing_tasks = session.query(Task).filter_by(user_id=default_user.id).count()
    if existing_tasks == 0:
        # Ensure that at least one category exists to associate with tasks
        if not category_objects:
            print("No categories available to associate with tasks.")
            return
        
        # Create tasks
        tasks = [
            {
                "description": "Complete project report",
                "due_date": datetime(2024, 9, 25).date(),
                "priority": 2,
                "status": False,
                "category": "Work"
            },
            {
                "description": "Buy groceries",
                "due_date": datetime(2024, 9, 22).date(),
                "priority": 1,
                "status": False,
                "category": "Personal"
            },
            {
                "description": "Gym session",
                "due_date": datetime(2024, 9, 21).date(),
                "priority": 3,
                "status": False,
                "category": "Health"
            }
        ]
        
        for task_data in tasks:
            category = session.query(Category).filter_by(name=task_data["category"]).first()
            if not category:
                # This should not happen as we've already created default categories
                category = Category(name=task_data["category"])
                session.add(category)
                session.commit()
            
            new_task = Task(
                description=task_data["description"],
                due_date=task_data["due_date"],
                priority=task_data["priority"],
                status=task_data["status"],
                category_id=category.id,
                user_id=default_user.id
            )
            session.add(new_task)
            print(f"Added task: {new_task.description} under category: {category.name}")
        
        session.commit()
        print("Tasks seeded successfully.")
    else:
        print("Tasks already exist for the default user.")

if __name__ == "__main__":
    seed()
