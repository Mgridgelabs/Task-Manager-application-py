# Task-Manager-application-py
A command-line application built using Python, SQLAlchemy, and Alembic, allowing users to manage their tasks with features like registering, logging in, adding, editing, viewing, and deleting tasks. The application uses a SQLite database to store user and task data.

## Features

- **User Registration and Login**: Users can register and log in using their email and password.
- **Task Management**: Add, view, edit, and delete tasks associated with the logged-in user.
- **Categories**: Tasks can be organized by categories. New categories can be created when adding tasks.
- **Task Prioritization**: Tasks have priority levels (1 = Low, 2 = Medium, 3 = High).
- **Mark as Complete**: Users can mark tasks as complete.

## Requirements

- Python 3.7+
- SQLAlchemy
- Alembic
- Click

## Usage
Run the application by executing:
- python cli.py

## Menu Options
- Register: Create a new user account.
- Login: Log in to an existing account.
- Add Task: Add a new task with description, due date, priority, and category.
- View Tasks: View all tasks of the logged-in user.
- Mark Task as Complete: Mark a specific task as complete.
- Edit Task: Modify a task's details, including description, due date, priority, and category.
- Delete Task: Permanently delete a task.
- Exit: Exit the application.

## Example Workflow
* Register a User:

- Choose the "Register" option from the menu.
- Enter your name, email, and password.

* Login:

- Choose the "Login" option.
- Provide your email and password to log in.

* Add a Task:

- After logging in, choose "Add Task".
- Provide task description, due date, priority, and category.

* View Tasks:

- Select "View Tasks" to list all tasks associated with the logged-in user.

* Edit or Delete Tasks:

Use "Edit Task" or "Delete Task" to modify or remove tasks.
