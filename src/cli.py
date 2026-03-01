
import argparse

def setup_cli():
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool"
    )

    subparsers = parser.add_subparsers(dest="command")


    add_user = subparsers.add_parser("add-user")
    add_user.add_argument("name")

   
    subparsers.add_parser("list-users")

  
    add_project = subparsers.add_parser("add-project")
    add_project.add_argument("user_id", type=int)
    add_project.add_argument("title")


    complete_task = subparsers.add_parser("complete-task")
    complete_task.add_argument("task_id", type=int)

    return parser