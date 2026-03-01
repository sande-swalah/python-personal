from models.task import Task

def test_task_completion():
    task = Task("Test task")
    task.mark_complete()
    assert task.completed is True