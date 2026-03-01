from .person import Person

class User(Person):
    _id_counter = 1

    def __init__(self, name):
        super().__init__(name)
        self.id = User._id_counter
        self.projects = []
        User._id_counter += 1

    def add_project(self, project):
        self.projects.append(project)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}')"