import sqlite3
from datetime import date, datetime

import click
from rich import box
from rich.console import Console
from rich.table import Table

# Connecting to SQLite database
conn = sqlite3.connect('todo.db')
c = conn.cursor()

# Check if 'tasks' table exists, and if not, create it
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
             )''')
conn.commit()

# Function to add a task
def add_task(task):
    c.execute('''INSERT INTO tasks (task, status) VALUES (?, ?)''', (task, 'Pending'))
    conn.commit()

# Function to delete a task
def delete_task(task_id):
    c.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
    conn.commit()

# Function to mark a task as done
def mark_as_done(task_id):
    c.execute('''UPDATE tasks SET status = 'Done' WHERE id = ?''', (task_id,))
    conn.commit()

# Function to show all tasks
def show_tasks():
    c.execute('''SELECT * FROM tasks''')
    tasks = c.fetchall()
    display_tasks(tasks)

# Function to show today's tasks
def show_today_tasks():
    today_date = date.today()
    c.execute('''SELECT * FROM tasks WHERE DATE(timestamp) = ?''', (str(today_date),))
    tasks = c.fetchall()
    display_tasks(tasks, f"Tasks for {today_date}:")

# Function to display tasks in a formatted table
def display_tasks(tasks, header=None):
    if tasks:
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
        table.add_column("ID", style="cyan", justify="center", width=5)
        table.add_column("Task", style="dim", width=50)
        table.add_column("Status", style="yellow", justify="center", width=15)
        table.add_column("Timestamp", style="dim", width=25)
        for task in tasks:
            table.add_row(str(task[0]), task[1], task[2], task[3])
        console = Console()
        if header:
            console.print(header)
        console.print(table)
    else:
        console = Console()
        console.print("No tasks found.")

# Function to export tasks to a file
def export_tasks(filename):
    c.execute('''SELECT * FROM tasks''')
    tasks = c.fetchall()
    with open(filename, 'w') as f:
        for task in tasks:
            f.write(f"{task[0]}, {task[1]}, {task[2]}, {task[3]}\n")

# Function to import tasks from a file
def import_tasks(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            task_id, task, status, timestamp = line.strip().split(', ')
            c.execute('''INSERT INTO tasks (id, task, status, timestamp) VALUES (?, ?, ?, ?)''', (task_id, task, status, timestamp))
    conn.commit()

# CLI commands setup using Click
@click.group()
def cli():
    pass

@cli.command()
@click.argument('task')
def add(task):
    add_task(task)
    click.echo('Task added successfully!')

@cli.command()
def show():
    show_tasks()

@cli.command()
def today():
    show_today_tasks()

@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    delete_task(task_id)
    click.echo('Task deleted successfully!')

@cli.command()
@click.argument('task_id', type=int)
def done(task_id):
    mark_as_done(task_id)
    click.echo('Task marked as done!')

@cli.command()
@click.argument('filename', type=str)
def export(filename):
    export_tasks(filename)
    click.echo(f'Tasks exported to {filename}')

@cli.command()
@click.argument('filename', type=str)
def import_file(filename):
    import_tasks(filename)
    click.echo(f'Tasks imported from {filename}')

if __name__ == '__main__':
    cli()
