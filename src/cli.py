
import argparse
import sys
import json
import os

from .models import User, Project, Task

from rich.console import Console
from rich.table import Table

# data file path (tests can override)
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')


def save_data(data) -> None:
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    except IOError as e:
        print(f"Error saving data: {e}")


def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {'users': []}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading data: {e}")
        return {'users': []}


def load():
    data = load_data()
    global users
    users = []
    for udata in data.get('users', []):
        users.append(User.from_dict(udata))


def save():
    """Persist current in-memory state to disk."""
    save_data({'users': [u.to_dict() for u in users]})

console = Console()


users: list[User] = []



def list_users(args):
    if not users:
        console.print("[yellow]No users available.[/yellow]")
        return
    table = Table(title="Users")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Email")
    for u in users:
        table.add_row(str(u.id), u.name, u.email)
    console.print(table)


def add_user(args):
    user = User(args.name, args.email)
    users.append(user)
    save()
    print(f"Created user {user}")


def add_project(args):
    user = find_user_by_id(args.user_id)
    if not user:
        print(f"User {args.user_id} not found.")
        return
    project = Project(args.title, args.description or "")
    user.add_project(project)
    save()
    print(f"Added project {project} to user {user}")


def list_projects(args):
    user = find_user_by_id(args.user_id)
    if not user:
        print(f"User {args.user_id} not found.")
        return
    projects = user.projects
    if getattr(args, 'search', None):
        query = args.search.lower()
        projects = [p for p in projects if query in p.title.lower()]
    if not projects:
        print("No projects for this user.")
        return
    for p in projects:
        print(p)


def add_task(args):
    user = find_user_by_id(args.user_id)
    if not user:
        print(f"User {args.user_id} not found.")
        return
    project = next((p for p in user.projects if p.id == args.project_id), None)
    if not project:
        print(f"Project {args.project_id} not found for user {user.id}.")
        return
    task = Task(args.title)
    project.add_task(task)
    save()
    print(f"Added task {task} to project {project}")


def list_tasks(args):
    user = find_user_by_id(args.user_id)
    if not user:
        console.print(f"[red]User {args.user_id} not found.[/red]")
        return
    project = next((p for p in user.projects if p.id == args.project_id), None)
    if not project:
        console.print(f"[red]Project {args.project_id} not found for user {user.id}.[/red]")
        return
    if not project.tasks:
        console.print("[yellow]No tasks for this project.[/yellow]")
        return
    table = Table(title=f"Tasks for {project.title}")
    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Completed")
    for t in project.tasks:
        table.add_row(str(t.id), t.title, "✔" if t.completed else "")
    console.print(table)


def complete_task(args):
    user = find_user_by_id(args.user_id)
    if not user:
        console.print(f"[red]User {args.user_id} not found.[/red]")
        return
    project = next((p for p in user.projects if p.id == args.project_id), None)
    if not project:
        console.print(f"[red]Project {args.project_id} not found for user {user.id}.[/red]")
        return
    task = next((t for t in project.tasks if t.id == args.task_id), None)
    if not task:
        console.print(f"[red]Task {args.task_id} not found in project {project.id}.[/red]")
        return
    task.mark_complete()
    save()
    console.print(f"[green]Marked task {task.id} as complete.[/green]")


def main():
    parser = argparse.ArgumentParser(description="Project management CLI tool")
    subparsers = parser.add_subparsers(title="commands")

    # user commands
    parser_add_user = subparsers.add_parser('add-user', help='Create a new user')
    parser_add_user.add_argument('name')
    parser_add_user.add_argument('email')
    parser_add_user.set_defaults(func=add_user)

    parser_list_users = subparsers.add_parser('list-users', help='List all users')
    parser_list_users.set_defaults(func=list_users)

    # project commands
    parser_add_proj = subparsers.add_parser('add-project', help='Add project to a user')
    parser_add_proj.add_argument('user_id', type=int)
    parser_add_proj.add_argument('title')
    parser_add_proj.add_argument('--description', '-d', help='Description of project')
    parser_add_proj.set_defaults(func=add_project)

    parser_list_proj = subparsers.add_parser('list-projects', help='List projects for user')
    parser_list_proj.add_argument('user_id', type=int)
    parser_list_proj.add_argument('--search', '-s', help='Filter projects by title substring')
    parser_list_proj.set_defaults(func=list_projects)

    # task commands
    parser_add_task = subparsers.add_parser('add-task', help='Add task to a project')
    parser_add_task.add_argument('user_id', type=int)
    parser_add_task.add_argument('project_id', type=int)
    parser_add_task.add_argument('title')
    parser_add_task.set_defaults(func=add_task)

    parser_list_task = subparsers.add_parser('list-tasks', help='List tasks in project')
    parser_list_task.add_argument('user_id', type=int)
    parser_list_task.add_argument('project_id', type=int)
    parser_list_task.set_defaults(func=list_tasks)

    parser_complete = subparsers.add_parser('complete-task', help='Mark task complete')
    parser_complete.add_argument('user_id', type=int)
    parser_complete.add_argument('project_id', type=int)
    parser_complete.add_argument('task_id', type=int)
    parser_complete.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        load()
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
