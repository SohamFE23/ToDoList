import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Function to connect to the database
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Admin@2205',
        database='todo_db'
    )

# Function to add a new task
def add_task():
    task = task_entry.get()
    if task:
        cnx = create_connection()
        cursor = cnx.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
        cnx.commit()
        cursor.close()
        cnx.close()
        task_entry.delete(0, tk.END)
        populate_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Function to populate tasks from the database
def populate_tasks():
    for item in task_tree.get_children():
        task_tree.delete(item)
    cnx = create_connection()
    cursor = cnx.cursor()
    cursor.execute('SELECT id, task, completed FROM tasks')
    for task_id, task, completed in cursor.fetchall():
        task_tree.insert('', tk.END, iid=task_id, text='', values=(task, completed), tags=('completed' if completed else 'pending',))
    cursor.close()
    cnx.close()

# Function to toggle task completion
def toggle_task_completion(event):
    selected_item = task_tree.focus()
    if selected_item:
        current_values = task_tree.item(selected_item, 'values')
        task_id = selected_item
        task_name = current_values[0]
        completed = not current_values[1]  # Switch the completion status
        cnx = create_connection()
        cursor = cnx.cursor()
        cursor.execute('UPDATE tasks SET completed = %s WHERE id = %s', (completed, task_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        populate_tasks()

# Initialize the main application window
root = tk.Tk()
root.title("To-Do List")
root.geometry("500x400")

# Entry field for a new task
task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=10)

# Button to add a task
add_task_button = tk.Button(root, text="Add Task", command=add_task)
add_task_button.pack(pady=5)

# Treeview to display tasks
columns = ('Task', 'Completed')
task_tree = ttk.Treeview(root, columns=columns, show='headings', selectmode='browse')
task_tree.heading('Task', text='Task')
task_tree.heading('Completed', text='Completed')
task_tree.bind('<Double-1>', toggle_task_completion)  # Bind double-click event to toggle completion
task_tree.pack(pady=10, fill='both', expand=True)

# Initial population of the task list
populate_tasks()

# Running the application
root.mainloop()
