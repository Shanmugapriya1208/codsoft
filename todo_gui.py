import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store the tasks
TASKS_FILE = 'tasks.json'

# Function to load tasks from the file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

# Function to save tasks to the file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Main application class
class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")
        self.geometry("400x400")
        self.tasks = load_tasks()
        
        self.create_widgets()
        self.display_tasks()

    def create_widgets(self):
        self.task_entry = tk.Entry(self, width=40)
        self.task_entry.pack(pady=10)
        
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.tasks_listbox = tk.Listbox(self, width=50, height=15)
        self.tasks_listbox.pack(pady=10)
        
        self.update_button = tk.Button(self, text="Update Task", command=self.update_task)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def display_tasks(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, f"{task['id']}. {task['description']} [{task['status']}]")

    def add_task(self):
        task_description = self.task_entry.get().strip()
        if task_description:
            task_id = len(self.tasks) + 1
            self.tasks.append({"id": task_id, "description": task_description, "status": "pending"})
            save_tasks(self.tasks)
            self.display_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty")

    def update_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            selected_task = self.tasks[selected_index]
            new_description = self.task_entry.get().strip()
            if new_description:
                selected_task['description'] = new_description
                selected_task['status'] = 'completed' if selected_task['status'] == 'pending' else 'pending'
                save_tasks(self.tasks)
                self.display_tasks()
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", "Task description cannot be empty")
        except IndexError:
            messagebox.showwarning("Warning", "No task selected")

    def delete_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            self.tasks.pop(selected_index)
            save_tasks(self.tasks)
            self.display_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected")

if __name__ == '__main__':
    app = ToDoApp()
    app.mainloop()
