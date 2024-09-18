from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Task, Category, Base
import click
from getpass import getpass

# Create an engine and a session
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)

# Command group class to list commands in a specific order
class OrderedGroup(click.Group):
    def list_commands(self, ctx):
        commands = super().list_commands(ctx)
        order = ['register', 'login', 'add-task', 'view-tasks', 'mark-complete', 'edit-task', 'delete-task']
        return [cmd for cmd in order if cmd in commands]

@click.group(cls=OrderedGroup)
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
    session = Session()
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        click.echo("Email already exists. Please choose a different one.")
        session.close()
        return

    # Create new user & save
    new_user = User(name=name, email=email, password=password)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    session.close()
    click.echo(f"User {name} registered successfully!")

# Login
@cli.command()
def login():
    """Login an existing user"""
    click.echo("Login:")
    email = click.prompt("Enter your email")
    password = getpass("Enter your password")

    session = Session()
    user = session.query(User).filter_by(email=email).first()
    if not user or not user.check_password(password):
        click.echo("Invalid email or password. Please try again.")
        session.close()
        return

    global current_user
    current_user = user
    session.close()
    click.echo(f"Welcome, {user.name}!")

# Add Task
@cli.command()
@click.option('--description', prompt="Task description", help="The description of the task")
@click.option('--due_date', prompt="Due date (YYYY-MM-DD)", help="The due date for the task")
@click.option('--priority', prompt="Priority (1: Low, 2: Medium, 3: High)", type=int)
@click.option('--category', prompt="Category", help="The category of the task")
def add_task(description, due_date, priority, category):
    """Add a new task"""
    if 'current_user' not in globals():
        click.echo("You need to login first!")
        return

    session = Session()
    task_category = session.query(Category).filter_by(name=category).first()
    if not task_category:
        task_category = Category(name=category)
        session.add(task_category)
        session.commit()

    new_task = Task(
        description=description,
        due_date=due_date,
        priority=priority,
        status=False,
        category_id=task_category.id,
        user_id=current_user.id
    )
    session.add(new_task)
    session.commit()
    session.close()
    click.echo(f"Task '{description}' added successfully!")

# Mark Task as Completed
@cli.command()
@click.option('--task_id', prompt="Task ID", help="The ID of the task to mark complete", type=int)
def mark_complete(task_id):
    """Mark a task as complete"""
    session = Session()
    task = session.query(Task).get(task_id)

    if not task:
        click.echo("Error: Task not found.")
        session.close()
        return

    task.status = True
    session.commit()
    session.close()
    click.echo(f"Task '{task.description}' marked as complete!")

# View Tasks
@cli.command()
def view_tasks():
    """View all tasks for the current user"""
    if 'current_user' not in globals():
        click.echo("You need to login first!")
        return

    session = Session()
    tasks = session.query(Task).filter_by(user_id=current_user.id).all()

    if not tasks:
        click.echo("No tasks found.")
        session.close()
        return

    for task in tasks:
        status = "Complete" if task.status else "Incomplete"
        click.echo(f"[{task.id}] {task.description} | Due: {task.due_date} | Priority: {task.priority} | Status: {status}")
    
    session.close()

# Delete Task
@cli.command()
@click.option('--task_id', prompt="Task ID", help="The ID of the task to delete", type=int)
def delete_task(task_id):
    """Delete a task by its ID"""
    session = Session()
    task = session.query(Task).get(task_id)

    if not task:
        click.echo("Error: Task not found.")
        session.close()
        return

    session.delete(task)
    session.commit()
    session.close()
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
    session = Session()
    task = session.query(Task).get(task_id)

    if not task:
        click.echo("Error: Task not found.")
        session.close()
        return

    task.description = description
    task.due_date = due_date
    task.priority = priority

    task_category = session.query(Category).filter_by(name=category).first()
    if not task_category:
        task_category = Category(name=category)
        session.add(task_category)
        session.commit()

    task.category_id = task_category.id
    session.commit()
    session.close()
    click.echo(f"Task '{task.description}' updated successfully!")

if __name__ == '__main__':
    while True:
        click.echo("\nPersonal Task Manager")
        click.echo("1. Register")
        click.echo("2. Login")
        click.echo("3. Add Task")
        click.echo("4. View Tasks")
        click.echo("5. Mark Task as Complete")
        click.echo("6. Edit Task")
        click.echo("7. Delete Task")
        click.echo("8. Exit")
        
        choice  = click.prompt("Choose an option", type=int)
        
        if choice == 1:
            cli.invoke(cli.commands['register'])
        elif choice == 2:
            cli.invoke(cli.commands['login'])
        elif choice == 3:
            cli.invoke(cli.commands['add-task'])
        elif choice == 4:
            cli.invoke(cli.commands['view-tasks'])
        elif choice == 5:
            cli.invoke(cli.commands['mark-complete'])
        elif choice == 6:
            cli.invoke(cli.commands['edit-task'])
        elif choice == 7:
            cli.invoke(cli.commands['delete-task'])
        elif choice == 8:
            break
        else:
            click.echo("Invalid option, please try again.")
