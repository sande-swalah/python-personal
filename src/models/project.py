class Project:
    _id_counter = 1

    def __init__(self, title, owner_id):
        self.id = Project._id_counter
        self.title = title
        self.owner_id = owner_id
        self.tasks = []
        Project._id_counter += 1

    def add_task(self, task):
        self.tasks.append(task)

    def __repr__(self):
        return f"Project(id={self.id}, title='{self.title}')"