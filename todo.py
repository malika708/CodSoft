import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime

class TodoAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced To-Do List")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.tasks = self.load_tasks()

        # Custom Fonts and Colors
        self.custom_font = ("Helvetica", 12)
        self.custom_button_font = ("Helvetica", 10, "bold")
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.delete_button_color = "#FF5252"
        self.root.configure(bg=self.bg_color)

        # Widgets
        self.title_label = ttk.Label(root, text="Title:", font=self.custom_font, background=self.bg_color)
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.title_entry = ttk.Entry(root, width=50, font=self.custom_font)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        self.description_label = ttk.Label(root, text="Description:", font=self.custom_font, background=self.bg_color)
        self.description_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.description_entry = ttk.Entry(root, width=50, font=self.custom_font)
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        self.priority_label = ttk.Label(root, text="Priority:", font=self.custom_font, background=self.bg_color)
        self.priority_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.priority_combobox = ttk.Combobox(root, values=["Low", "Medium", "High"], font=self.custom_font, state="readonly")
        self.priority_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.priority_combobox.current(0)

        self.due_date_label = ttk.Label(root, text="Due Date (YYYY-MM-DD):", font=self.custom_font, background=self.bg_color)
        self.due_date_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.due_date_entry = ttk.Entry(root, width=50, font=self.custom_font)
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_button = tk.Button(root, text="Add Task", font=self.custom_button_font, bg=self.button_color, fg="white", command=self.add_task)
        self.add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.task_listbox = tk.Listbox(root, width=80, height=15, font=self.custom_font, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="Delete Task", font=self.custom_button_font, bg=self.delete_button_color, fg="white", command=self.delete_task)
        self.delete_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.toggle_button = tk.Button(root, text="Toggle Status", font=self.custom_button_font, bg=self.button_color, fg="white", command=self.toggle_status)
        self.toggle_button.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        # Drag-and-Drop for Reordering
        self.task_listbox.bind("<ButtonPress-1>", self.on_start)
        self.task_listbox.bind("<B1-Motion>", self.on_drag)
        self.task_listbox.bind("<ButtonRelease-1>", self.on_drop)

        self.display_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        priority = self.priority_combobox.get()
        due_date = self.due_date_entry.get()

        if title and description and due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")  # Validate date format
                task = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "due_date": due_date,
                    "status": "Incomplete"
                }
                self.tasks.append(task)
                self.save_tasks()
                self.display_tasks()
                self.title_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showwarning("Date Error", "Please enter a valid date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_task_index]
            self.save_tasks()
            self.display_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def toggle_status(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            task["status"] = "Complete" if task["status"] == "Incomplete" else "Incomplete"
            self.save_tasks()
            self.display_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to toggle status.")

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            title = task["title"]
            description = task["description"]
            priority = task["priority"]
            due_date = task["due_date"]
            status = task["status"]
            display_text = f"{title} - {description} (Priority: {priority}, Due: {due_date}, Status: {status})"
            self.task_listbox.insert(tk.END, display_text)
            if status == "Complete":
                self.task_listbox.itemconfig(tk.END, {'fg': 'green'})
            else:
                self.task_listbox.itemconfig(tk.END, {'fg': 'black'})

    # Drag-and-Drop Functions
    def on_start(self, event):
        self.drag_index = self.task_listbox.nearest(event.y)

    def on_drag(self, event):
        new_index = self.task_listbox.nearest(event.y)
        if new_index < self.drag_index:
            x, y, width, height = self.task_listbox.bbox(new_index)
            self.task_listbox.yview_scroll(-1, "units")
        elif new_index > self.drag_index:
            x, y, width, height = self.task_listbox.bbox(new_index)
            self.task_listbox.yview_scroll(1, "units")

    def on_drop(self, event):
        new_index = self.task_listbox.nearest(event.y)
        if new_index != self.drag_index:
            task = self.tasks.pop(self.drag_index)
            self.tasks.insert(new_index, task)
            self.save_tasks()
            self.display_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoAppGUI(root)
    root.mainloop()