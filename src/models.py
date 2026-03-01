

import json
from typing import List, Dict


class Person:
    _id_counter = 1

    def __init__(self, name, email):
        self.id = Person._id_counter
        Person._id_counter += 1
        self.name = name
        self.email = email

    def __str__(self):
        return f"[{self.id}] {self.name} <{self.email}>"


class User(Person):

    def __init__(self, name, email):
        super().__init__(name, email)
        self.projects: List[Project] = []  # type: ignore # forward reference

    def add_project(self, project: 'Project') -> None:  # type: ignore
        self.projects.append(project)

    def list_projects(self) -> List['Project']:
        return self.projects

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'projects': [p.to_dict() for p in self.projects],
        }

    @classmethod
    def from_dict(cls, data) -> 'User':
        user = cls(data['name'], data['email'])
        user.id = data['id']
        cls._id_counter = max(cls._id_counter, user.id + 1)
        for p_data in data.get('projects', []):
            project = Project.from_dict(p_data)
            user.add_project(project)
        return user


class Project:
    _id_counter = 1

    def __init__(self, title, description):
        self.id = Project._id_counter
        Project._id_counter += 1
        self.title = title
        self.description = description
        self.tasks: List[Task] = []  # type: ignore

    def add_task(self, task: 'Task') -> None:  # type: ignore
        self.tasks.append(task)

    def list_tasks(self) -> List['Task']:
        return self.tasks

    def __str__(self):
        return f"[{self.id}] {self.title}: {self.description}"

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title})"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tasks': [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        project = cls(data['title'], data.get('description', ''))
        project.id = data['id']
        cls._id_counter = max(cls._id_counter, project.id + 1)
        for t_data in data.get('tasks', []):
            task = Task.from_dict(t_data)
            project.add_task(task)
        return project


class Task:
    _id_counter = 1

    def __init__(self, title):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "Done" if self.completed else "not done"
        return f"[{self.id}] {self.title} {status}"

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, completed={self.completed})"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        task = cls(data['title'])
        task.id = data['id']
        task.completed = data.get('completed', False)
        cls._id_counter = max(cls._id_counter, task.id + 1)
        return task
