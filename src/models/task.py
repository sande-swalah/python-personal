class Task:
    _id_counter = 1

    def __init__(self, description, contributors=None):
        self.id = Task._id_counter
        self.description = description
        self.completed = False
        self.contributors = contributors if contributors else []
        Task._id_counter += 1

    def mark_complete(self):
        self.completed = True

    def __repr__(self):
        return f"Task(id={self.id}, completed={self.completed})"