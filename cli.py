import click
from sqlalchemy import sessionmaker
from models import User, Task, Category, engine
from getpass import getpass  # hides password input

# Create a new session for database operations
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """Personal Task Manager"""
    pass

# Register
@cli.command()
def register():
    """Register a new user"""
    click.echo("Register a new user:")
    name = click.prompt("Enter your name")
    email = click.prompt("Enter your email address")
    password = getpass("Enter your password")

    # Check if email already exists
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        click.echo("Email already exists. Please choose a different one.")
        return

    # Create new user & save
    new_user = User(name=name, email=email, password=password)
    session.add(new_user)
    session.commit()
    click.echo(f"User {name} registered successfully!")

# Login
@cli.command()
def login():
    """Login an existing user"""
    click.echo("Login:")
    email = click.prompt("Enter your email")
    password = getpass("Enter your password")

    # Check if user exists
    user = session.query(User).filter_by(email=email, password=password).first()
    if not user:
        click.echo("Invalid email or password. Please try again.")
        return

    global current_user
    current_user = user
    click.echo(f"Welcome, {user.name}!")  # Store user in session

# Task Manager
@cli.command()
@click.option('--description', prompt="Task description", help="The description of the task")
@click.option('--due_date', prompt="Due date (YYYY-MM-DD)", help="The due date for the task")
@click.option('--priority', prompt="Priority (1: Low, 2: Medium, 3: High)", type=int)
@click.option('--category', prompt="Category", help="The category of the task")
def add_task(description, due_date, priority, category):
    """Add a new task"""
    # Ensure the user is logged in
    if 'current_user' not in globals():
        click.echo("You need to login first!")
        return
    
    # Check if category exists, else create
    task_category = session.query(Category).filter_by(name=category).first()
    if not task_category:
        task_category = Category(name=category)
        session.add(task_category)
        session.commit()

    # Create task
    new_task = Task(
        description=description,
        due_date=due_date,
        priority=priority,
        status=False,
        category_id=task_category.id,
        user_id=current_user.id  # Using logged-in user's ID
    )
    session.add(new_task)
    session.commit()
    click.echo(f"Task '{description}' added successfully!")

# Mark Task as Completed
@cli.command()
@click.option('--task_id', prompt="Task ID", help="The ID of the task to mark complete", type=int)
def mark_complete(task_id):
    """Mark a task as complete"""
    task = session.query(Task).get(task_id)

    if not task:
        click.echo("Error: Task not found.")
        return

    task.status = True
    session.commit()
    click.echo(f"Task '{task.description}' marked as complete!")

# View Tasks
@cli.command()
def view_tasks():
    """View all tasks for the current user"""
    if 'current_user' not in globals():
        click.echo("You need to login first!")
        return
    
    tasks = session.query(Task).filter_by(user_id=current_user.id).all()

    if not tasks:
        click.echo("No tasks found.")
        return

    for task in tasks:
        status = "Complete" if task.status else "Incomplete"
        click.echo(f"[{task.id}] {task.description} | Due: {task.due_date} | Priority: {task.priority} | Status: {status}")

# Delete Task
@cli.command()
@click.option('--task_id', prompt="Task ID", help="The ID of the task to delete", type=int)
def delete_task(task_id):
    """Delete a task by its ID"""
    task = session.query(Task).get(task_id)

    if not task:
        click.echo("Error: Task not found.")
        return

    session.delete(task)
    session.commit()
    click.echo(f"Task '{task.description}' deleted successfully!")

# Edit Task
@cli.command()
@click.option('--task_id', prompt="Task ID", help="The ID of the task to update", type=int)
@click.option('--description', prompt="New description", help="Update the task description")
@click.option('--due_date', prompt="New due date (YYYY-MM-DD)", help="Update the due date")
@click.option('--priority', prompt="New priority (1: Low, 2: Medium, 3: High)", type=int)
@click.option('--category', prompt="New category", help="Update the category for the task")
def edit_task(task_id, description, due_date, priority, category):
    """Edit a task by its ID"""
    task = session.query(Task).get(task_id)

    if not task:
        click.echo("Error: Task not found.")
        return

    # Update task details
    task.description = description
    task.due_date = due_date
    task.priority = priority

    # Update category if needed
    task_category = session.query(Category).filter_by(name=category).first()
    if not task_category:
        task_category = Category(name=category)
        session.add(task_category)
        session.commit()

    task.category_id = task_category.id

    session.commit()
    click.echo(f"Task '{task.description}' updated successfully!")
