# dao/task_dao.py
import sqlite3
from models.task import Task

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT,
                  completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))''')
    conn.commit()
    conn.close()

init_db()

def get_all_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    tasks = [Task(row[0], row[1], row[2], row[3]) for row in rows]
    conn.close()
    return tasks

def add_task(title, description):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
              (title, description, False))
    conn.commit()
    conn.close()

def update_task_status(task_id, completed):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, title, description):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET title = ?, description = ? WHERE id = ?", (title, description, task_id))
    conn.commit()
    conn.close()
