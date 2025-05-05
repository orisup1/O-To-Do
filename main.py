import tkinter as tk
from tkinter import messagebox, ttk

# Global task lists
tasks = []
completed_tasks = []

# Task creation
def create_task(title, due):
    return {"title": title, "due": due, "done": False}

# Add task
def add_task(event=None):
    name = task_name_entry.get().strip()
    date = due_date_entry.get().strip()
    if not name or not date:
        messagebox.showwarning("Input Error", "Please enter both task name and due date.")
        return
    tasks.append(create_task(name, date))
    update_task_list()
    task_name_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)

# Remove task
def remove_task(event=None):
    selected = task_listbox.get(tk.ACTIVE)
    if selected:
        title = selected.split(" (Due:")[0]
        update_tasks(lambda t: t["title"] != title)
        update_task_list()
    else:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")

# Mark task as complete
def complete_task(event=None):
    selected = task_listbox.get(tk.ACTIVE)
    if selected:
        title = selected.split(" (Due:")[0]
        move_task_to_completed(title)
        update_task_list()
    else:
        messagebox.showwarning("Selection Error", "Please select a task to complete.")

# Move to completed
def move_task_to_completed(title):
    global tasks, completed_tasks
    for task in tasks:
        if task["title"] == title:
            task["done"] = True
            completed_tasks.append(task)
            tasks = [t for t in tasks if t["title"] != title]
            break

# Update tasks by filter
def update_tasks(predicate):
    global tasks
    tasks[:] = list(filter(predicate, tasks))

# Clear all tasks
def clear_tasks(event=None):
    tasks.clear()
    update_task_list()

# Clear completed
def clear_completed_tasks(event=None):
    completed_tasks.clear()
    update_task_list()

# Quit app
def quit_app(event=None):
    root.quit()

# Refresh listboxes
def update_task_list():
    task_listbox.delete(0, tk.END)
    completed_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, f"{task['title']} (Due: {task['due']})")
    for task in completed_tasks:
        completed_listbox.insert(tk.END, f"{task['title']} (Completed)")

# --- GUI Setup ---

root = tk.Tk()
root.title("Task Manager")
root.geometry("820x520")
root.configure(bg="#1e1e1e")

style = ttk.Style(root)
style.theme_use("clam")

bg_color = "#1e1e1e"
fg_color = "#ffffff"
entry_bg = "#2b2b2b"
highlight_color = "#3c3c3c"
button_bg = "#444"
button_fg = "#fff"

style.configure(".", background=bg_color, foreground=fg_color, fieldbackground=entry_bg)
style.configure("TEntry", padding=5)
style.configure("TButton", background=button_bg, foreground=button_fg, padding=6)
style.map("TButton", background=[("active", "#666")])
style.configure("TLabel", background=bg_color, foreground=fg_color)

top_frame = ttk.Frame(root, padding=10)
top_frame.pack(fill="x")

ttk.Label(top_frame, text="Task Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
task_name_entry = ttk.Entry(top_frame, width=30)
task_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(top_frame, text="Due Date:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
due_date_entry = ttk.Entry(top_frame, width=20)
due_date_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Button(top_frame, text="Add Task", command=add_task).grid(row=0, column=4, padx=5)

middle_frame = ttk.Frame(root, padding=10)
middle_frame.pack(fill="both", expand=True)

ttk.Label(middle_frame, text="Pending Tasks:").grid(row=0, column=0, sticky="w")
task_listbox = tk.Listbox(middle_frame, height=10, width=60, bg=entry_bg, fg=fg_color, selectbackground=highlight_color)
task_listbox.grid(row=1, column=0, columnspan=3, pady=5)

btn_frame = ttk.Frame(middle_frame)
btn_frame.grid(row=1, column=3, padx=10)

ttk.Button(btn_frame, text="Complete", command=complete_task).pack(fill="x", pady=2)
ttk.Button(btn_frame, text="Remove", command=remove_task).pack(fill="x", pady=2)
ttk.Button(btn_frame, text="Clear All", command=clear_tasks).pack(fill="x", pady=2)

ttk.Label(middle_frame, text="Completed Tasks:").grid(row=2, column=0, pady=(10, 0), sticky="w")
completed_listbox = tk.Listbox(middle_frame, height=8, width=60, bg=entry_bg, fg=fg_color, selectbackground=highlight_color)
completed_listbox.grid(row=3, column=0, columnspan=3, pady=5)

ttk.Button(middle_frame, text="Clear Completed", command=clear_completed_tasks).grid(row=3, column=3)

bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.pack(fill="x")

ttk.Button(bottom_frame, text="Quit", command=quit_app).pack(side="right")

# Shortcuts
root.bind_all('<Command-a>', add_task)
root.bind_all('<Command-c>', complete_task)
root.bind_all('<Command-r>', remove_task)
root.bind_all('<Command-d>', clear_tasks)
root.bind_all('<Command-e>', clear_completed_tasks)
root.bind_all('<Command-q>', quit_app)

root.mainloop()
