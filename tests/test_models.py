import pytest
from datetime import datetime

from src.models import User, Project, Task


def test_user_project_task_relationship():
    user = User('Alice', 'alice@example.com')
    project = Project('Test', 'desc')
    task = Task('Do something', datetime(2025, 1, 1))
    project.add_task(task)
    user.add_project(project)

    assert user.projects[0] is project
    assert project.tasks[0] is task


def test_task_completion():
    t = Task('Any')
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_serialization_roundtrip(tmp_path):
    user = User('Bob', 'bob@ex.com')
    proj = Project('P', '')
    task = Task('T')
    proj.add_task(task)
    user.add_project(proj)
    data = user.to_dict()
    loaded = User.from_dict(data)
    assert loaded.name == user.name
    assert loaded.projects[0].title == proj.title
    assert loaded.projects[0].tasks[0].title == task.title
