# models/task.py
class Task:
    def __init__(self, id, title, description, completed):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed