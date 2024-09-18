# import click
# from sqlalchemy.orm import sessionmaker
# from models import User, Task, Category, engine
# from getpass import getpass  # hides password input

# # Create a new session for database operations
# Session = sessionmaker(bind=engine)
# session = Session()

# # Command group class (to list commands in a specific order)
# class OrderedGroup(click.Group):
#     def list_commands(self, ctx):
#         commands = super().list_commands(ctx)
#         order = ['register', 'login', 'add-task', 'view-tasks', 'mark-complete', 'edit-task', 'delete-task']
#         return [cmd for cmd in order if cmd in commands]

# @click.group(cls=OrderedGroup)
# def cli():
#     """Personal Task Manager"""
#     pass

# # Register
# @cli.command()
# def register():
#     """Register a new user"""
#     click.echo("Register a new user:")
#     name = click.prompt("Enter your name")
#     email = click.prompt("Enter your email address")
#     password = getpass("Enter your password")

#     # Check if email already exists
#     existing_user = session.query(User).filter_by(email=email).first()
#     if existing_user:
#         click.echo("Email already exists. Please choose a different one.")
#         return

#     # Create new user & save
#     new_user = User(name=name, email=email)
#     new_user.set_password(password)
#     session.add(new_user)
#     session.commit()
#     click.echo(f"User {name} registered successfully!")

# current_user = None  # Track the logged-in user

# # Login
# @cli.command()
# def login():
#     """Login an existing user"""
#     global current_user  # Ensure we're modifying the global current_user
#     click.echo("Login:")
#     email = click.prompt("Enter your email")
#     password = getpass("Enter your password")

#     # Check if user exists
#     user = session.query(User).filter_by(email=email).first()
#     if user:
#         click.echo(f"User found: {user.name}")
#         # Ensure password check works with hashed password
#         if user.check_password(password):
#             current_user = user  # Set the global current_user
#             click.echo(f"Welcome, {user.name}!")  # Store user in session
#         else:
#             click.echo("Invalid password.")
#     else:
#         click.echo("User not found.")

# # Add Task
# @cli.command()
# @click.option('--description', prompt="Task description", help="The description of the task")
# @click.option('--due_date', prompt="Due date (YYYY-MM-DD)", help="The due date for the task")
# @click.option('--priority', prompt="Priority (1: Low, 2: Medium, 3: High)", type=int)
# @click.option('--category', prompt="Category", help="The category of the task")
# def add_task(description, due_date, priority, category):
#     """Add a new task"""
#     global current_user  # Ensure we're accessing the global current_user

#     # Check if the user is logged in
#     if current_user is None:
#         click.echo("You need to login first!")
#         return
    
#     # Find or create the task category
#     task_category = session.query(Category).filter_by(name=category).first()
#     if not task_category:
#         task_category = Category(name=category)
#         session.add(task_category)
#         session.commit()

#     # Create a new task associated with the logged-in user
#     new_task = Task(
#         description=description,
#         due_date=due_date,
#         priority=priority,
#         status=False,  # Assuming new tasks are not complete by default
#         category_id=task_category.id,
#         user_id=current_user.id  # Associate task with logged-in user
#     )
#     session.add(new_task)
#     session.commit()
#     click.echo(f"Task '{description}' added successfully!")


# # Mark Task as Completed
# @cli.command()
# @click.option('--task_id', prompt="Task ID", help="The ID of the task to mark complete", type=int)
# def mark_complete(task_id):
#     """Mark a task as complete"""
#     task = session.query(Task).get(task_id)

#     if not task:
#         click.echo("Error: Task not found.")
#         return

#     task.status = True
#     session.commit()
#     click.echo(f"Task '{task.description}' marked as complete!")

# # View Tasks
# @cli.command()
# def view_tasks():
#     """View all tasks for the current user"""
#     if 'current_user' not in globals():
#         click.echo("You need to login first!")
#         return
    
#     tasks = session.query(Task).filter_by(user_id=current_user.id).all()

#     if not tasks:
#         click.echo("No tasks found.")
#         return

#     for task in tasks:
#         status = "Complete" if task.status else "Incomplete"
#         click.echo(f"[{task.id}] {task.description} | Due: {task.due_date} | Priority: {task.priority} | Status: {status}")

# # Delete Task
# @cli.command()
# @click.option('--task_id', prompt="Task ID", help="The ID of the task to delete", type=int)
# def delete_task(task_id):
#     """Delete a task by its ID"""
#     task = session.query(Task).get(task_id)

#     if not task:
#         click.echo("Error: Task not found.")
#         return

#     session.delete(task)
#     session.commit()
#     click.echo(f"Task '{task.description}' deleted successfully!")

# # Edit Task
# @cli.command()
# @click.option('--task_id', prompt="Task ID", help="The ID of the task to update", type=int)
# @click.option('--description', prompt="New description", help="Update the task description")
# @click.option('--due_date', prompt="New due date (YYYY-MM-DD)", help="Update the due date")
# @click.option('--priority', prompt="New priority (1: Low, 2: Medium, 3: High)", type=int)
# @click.option('--category', prompt="New category", help="Update the category for the task")
# def edit_task(task_id, description, due_date, priority, category):
#     """Edit a task by its ID"""
#     task = session.query(Task).get(task_id)

#     if not task:
#         click.echo("Error: Task not found.")
#         return

#     task.description = description
#     task.due_date = due_date
#     task.priority = priority

#     task_category = session.query(Category).filter_by(name=category).first()
#     if not task_category:
#         task_category = Category(name=category)
#         session.add(task_category)
#         session.commit()

#     task.category_id = task_category.id

#     session.commit()
#     click.echo(f"Task '{task.description}' updated successfully!")

# if __name__ == '__main__':
#     while True:
#         click.echo("\nPersonal Task Manager")
#         click.echo("1. Register")
#         click.echo("2. Login")
#         click.echo("3. Add Task")
#         click.echo("4. View Tasks")
#         click.echo("5. Mark Task as Complete")
#         click.echo("6. Edit Task")
#         click.echo("7. Delete Task")
#         click.echo("8. Exit")
        
#         choice = click.prompt("Choose an option", type=int)
        
#         if choice == 1:
#             cli(["register"])
#         elif choice == 2:
#             cli(["login"])
#         elif choice == 3:
#             cli(["add-task"])
#         elif choice == 4:
#             cli(["view-tasks"])
#         elif choice == 5:
#             cli(["mark-complete"])
#         elif choice == 6:
#             cli(["edit-task"])
#         elif choice == 7:
#             cli(["delete-task"])
#         elif choice == 8:
#             break
#         else:
#             click.echo("Invalid option, please try again.")

import click
from getpass import getpass
from models import User, Task, Category, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


# Set up database session
Session = sessionmaker(bind=engine)
session = Session()

current_user = None  # Track the logged-in user

# Menu options
def display_menu():
    click.echo("\nPersonal Task Manager")
    click.echo("1. Register")
    click.echo("2. Login")
    click.echo("3. Add Task")
    click.echo("4. View Tasks")
    click.echo("5. Mark Task as Complete")
    click.echo("6. Edit Task")
    click.echo("7. Delete Task")
    click.echo("8. Exit")

def register():
    """Register a new user"""
    click.echo("Register:")
    name = click.prompt("Enter your name")
    email = click.prompt("Enter your email")
    password = getpass("Enter your password")

    # Check if user already exists
    if session.query(User).filter_by(email=email).first():
        click.echo("User with this email already exists. Please login.")
        return

    new_user = User(name=name, email=email)
    new_user.set_password(password)  # Hash the password
    session.add(new_user)
    session.commit()
    click.echo(f"User '{name}' registered successfully!")

def login():
    """Login an existing user"""
    global current_user
    click.echo("Login:")
    email = click.prompt("Enter your email")
    password = getpass("Enter your password")

    # Check if user exists
    user = session.query(User).filter_by(email=email).first()
    if user:
        click.echo(f"User found: {user.name}")
        if user.check_password(password):
            current_user = user
            click.echo(f"Welcome, {user.name}!")
        else:
            click.echo("Invalid password.")
    else:
        click.echo("User not found.")

def add_task():
    """Add a new task"""
    global current_user
    if current_user is None:
        click.echo("You need to login first!")
        return
    
    description = click.prompt("Task description")
    due_date = click.prompt("Due date (YYYY-MM-DD)")
    priority = click.prompt("Priority (1: Low, 2: Medium, 3: High)", type=int)
    category = click.prompt("Category")

    # Find or create the task category
    task_category = session.query(Category).filter_by(name=category).first()
    if not task_category:
        task_category = Category(name=category)
        session.add(task_category)
        session.commit()

    # Create a new task
    new_task = Task(
        description=description,
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
        priority=priority,
        status=False,
        category_id=task_category.id,
        user_id=current_user.id
    )
    session.add(new_task)
    session.commit()
    click.echo(f"Task '{description}' added successfully!")

def view_tasks():
    """View all tasks for the current user"""
    global current_user
    if current_user is None:
        click.echo("You need to login first!")
        return

    tasks = session.query(Task).filter_by(user_id=current_user.id).all()

    if not tasks:
        click.echo("No tasks found.")
    else:
        click.echo(f"Tasks for {current_user.name}:")
        for task in tasks:
            status = "Complete" if task.status else "Incomplete"
            click.echo(f"{task.id}. {task.description} | Due: {task.due_date} | Priority: {task.priority} | Status: {status}")

def mark_task_complete():
    """Mark a task as complete"""
    global current_user
    if current_user is None:
        click.echo("You need to login first!")
        return
    
    task_id = click.prompt("Enter the Task ID to mark as complete", type=int)
    task = session.query(Task).filter_by(id=task_id, user_id=current_user.id).first()
    
    if task:
        task.status = True
        session.commit()
        click.echo(f"Task '{task.description}' marked as complete!")
    else:
        click.echo("Task not found.")

def edit_task():
    """Edit an existing task"""
    global current_user
    if current_user is None:
        click.echo("You need to login first!")
        return

    task_id = click.prompt("Enter the Task ID to edit", type=int)
    task = session.query(Task).filter_by(id=task_id, user_id=current_user.id).first()

    if task:
        click.echo("\nWhat would you like to edit?")
        click.echo("1. Description")
        click.echo("2. Due Date")
        click.echo("3. Priority")
        click.echo("4. Category")
        choice = click.prompt("Choose an option (1-4)", type=int)

        if choice == 1:
            new_description = click.prompt(f"New description (current: {task.description})", default=task.description)
            task.description = new_description
            click.echo(f"Task description updated to '{new_description}'")

        elif choice == 2:
            new_due_date = click.prompt(f"New due date (YYYY-MM-DD) (current: {task.due_date})", default=str(task.due_date))
            task.due_date = datetime.strptime(new_due_date, "%Y-%m-%d").date()
            click.echo(f"Task due date updated to '{new_due_date}'")

        elif choice == 3:
            new_priority = click.prompt(f"New priority (1: Low, 2: Medium, 3: High) (current: {task.priority})", type=int, default=task.priority)
            task.priority = new_priority
            click.echo(f"Task priority updated to '{new_priority}'")

        elif choice == 4:
            new_category = click.prompt(f"New category (current: {task.category.name})", default=task.category.name)
            task_category = session.query(Category).filter_by(name=new_category).first()
            if not task_category:
                task_category = Category(name=new_category)
                session.add(task_category)
                session.commit()
            task.category_id = task_category.id
            click.echo(f"Task category updated to '{new_category}'")

        else:
            click.echo("Invalid option. Please try again.")
            return

        session.commit()
        click.echo(f"Task '{task.description}' updated successfully!")
    else:
        click.echo("Task not found.")


def delete_task():
    """Delete a task"""
    global current_user
    if current_user is None:
        click.echo("You need to login first!")
        return

    task_id = click.prompt("Enter the Task ID to delete", type=int)
    task = session.query(Task).filter_by(id=task_id, user_id=current_user.id).first()

    if task:
        session.delete(task)
        session.commit()
        click.echo(f"Task '{task.description}' deleted successfully!")
    else:
        click.echo("Task not found.")

# Main loop
@click.command()
def main():
    while True:
        display_menu()
        choice = click.prompt("Choose an option", type=int)

        if choice == 1:
            register()
        elif choice == 2:
            login()
        elif choice == 3:
            add_task()
        elif choice == 4:
            view_tasks()
        elif choice == 5:
            mark_task_complete()
        elif choice == 6:
            edit_task()
        elif choice == 7:
            delete_task()
        elif choice == 8:
            click.echo("Exiting... Goodbye!")
            break
        else:
            click.echo("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
