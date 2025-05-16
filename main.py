import tkinter as tk
from tkinter import ttk, messagebox

# --- Task Storage ---
pending_tasks = []
finished_tasks = []

def make_task(name, due_date):
    return {"name": name, "due": due_date, "done": False}


# --- Task Actions ---
def on_add_task(event=None):
    name = task_name_entry.get().strip()
    due = due_date_entry.get().strip()

    if not name or not due:
        messagebox.showwarning("Missing Info", "Please enter both task name and due date.")
        return

    pending_tasks.append(make_task(name, due))
    refresh_task_display()

    task_name_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)


def on_complete_task(event=None):
    selected = task_listbox.get(tk.ACTIVE)
    if selected:
        name = selected.split(" (Due:")[0]
        for task in pending_tasks:
            if task["name"] == name:
                task["done"] = True
                finished_tasks.append(task)
                pending_tasks.remove(task)
                break
        refresh_task_display()


def on_remove_task(event=None):
    selected = task_listbox.get(tk.ACTIVE)
    if selected:
        name = selected.split(" (Due:")[0]
        pending_tasks[:] = [t for t in pending_tasks if t["name"] != name]
        refresh_task_display()


def on_clear_all_tasks(event=None):
    if messagebox.askyesno("Clear Tasks", "Are you sure you want to clear all tasks?"):
        pending_tasks.clear()
        refresh_task_display()


def on_clear_completed_tasks(event=None):
    if messagebox.askyesno("Clear Completed", "Clear all completed tasks?"):
        finished_tasks.clear()
        refresh_task_display()


def refresh_task_display():
    task_listbox.delete(0, tk.END)
    completed_listbox.delete(0, tk.END)

    for task in pending_tasks:
        task_listbox.insert(tk.END, f"{task['name']} (Due: {task['due']})")

    for task in finished_tasks:
        completed_listbox.insert(tk.END, f"{task['name']} (Completed)")


def quit_app(event=None):
    root.quit()


# --- GUI Setup ---
root = tk.Tk()
root.title("O_Task_Manager")
root.geometry("820x600")
root.configure(bg="#1e1e1e")  # Dark background

# --- Styles ---
style = ttk.Style()
style.theme_use("clam")

dark_bg = "#1e1e1e"
darker_bg = "#2c2c2e"
text_fg = "#ffffff"
highlight = "#444"

font_main = ("Helvetica Neue", 14)

style.configure("TFrame", background=dark_bg)
style.configure("TLabel", background=dark_bg, foreground=text_fg, font=font_main)
style.configure("TButton", background=darker_bg, foreground=text_fg,
                font=(font_main[0], 13, "bold"), padding=10)
style.map("TButton", background=[("active", "#3a3a3c")])
style.configure("TEntry", fieldbackground=darker_bg, foreground=text_fg,
                padding=6, font=font_main)

# --- Top Input ---
top_frame = ttk.Frame(root, padding=20)
top_frame.pack(fill="x")

ttk.Label(top_frame, text="Task:").grid(row=0, column=0, padx=5)
task_name_entry = ttk.Entry(top_frame, width=30)
task_name_entry.grid(row=0, column=1, padx=5)

ttk.Label(top_frame, text="Due:").grid(row=0, column=2, padx=5)
due_date_entry = ttk.Entry(top_frame, width=20)
due_date_entry.grid(row=0, column=3, padx=5)

ttk.Button(top_frame, text="Add Task", command=on_add_task).grid(row=0, column=4, padx=12)

# --- Task Lists ---
middle_frame = ttk.Frame(root, padding=20)
middle_frame.pack(fill="both", expand=True)

ttk.Label(middle_frame, text="Pending Tasks:").grid(row=0, column=0, sticky="w")
task_listbox = tk.Listbox(
    middle_frame, height=10, width=60, bg=darker_bg,
    fg=text_fg, selectbackground=highlight, font=font_main, relief="flat"
)
task_listbox.grid(row=1, column=0, columnspan=3, pady=5)

# Task Action Buttons
button_frame = ttk.Frame(middle_frame)
button_frame.grid(row=1, column=3, padx=20)

ttk.Button(button_frame, text="Complete", command=on_complete_task).pack(fill="x", pady=6)
ttk.Button(button_frame, text="Remove", command=on_remove_task).pack(fill="x", pady=6)
ttk.Button(button_frame, text="Clear All", command=on_clear_all_tasks).pack(fill="x", pady=6)

ttk.Label(middle_frame, text="Completed Tasks:").grid(row=2, column=0, pady=(20, 5), sticky="w")
completed_listbox = tk.Listbox(
    middle_frame, height=8, width=60, bg=darker_bg,
    fg=text_fg, selectbackground=highlight, font=font_main, relief="flat"
)
completed_listbox.grid(row=3, column=0, columnspan=3, pady=5)

ttk.Button(middle_frame, text="Clear Completed", command=on_clear_completed_tasks).grid(row=3, column=3, pady=10)

# --- Bottom Quit Button ---
bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.pack(fill="x")
ttk.Button(bottom_frame, text="Quit", command=quit_app).pack(side="right", padx=10)

# --- Shortcuts ---
root.bind_all('<Command-a>', on_add_task)
root.bind_all('<Command-c>', on_complete_task)
root.bind_all('<Command-r>', on_remove_task)
root.bind_all('<Command-d>', on_clear_all_tasks)
root.bind_all('<Command-e>', on_clear_completed_tasks)
root.bind_all('<Command-q>', quit_app)

root.mainloop()
