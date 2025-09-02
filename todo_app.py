
# To-Do List Application using Tkinter
# Step 2: Import Required Libraries

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os


# Step 3: Create the Main Application Class
class TodoApp:
	def save_tasks(self):
		try:
			with open("tasks.json", "w") as f:
				json.dump(self.tasks, f)
			messagebox.showinfo("Success", "Tasks saved successfully.")
		except Exception as e:
			messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")

	def load_tasks(self):
		if os.path.exists("tasks.json"):
			try:
				with open("tasks.json", "r") as f:
					self.tasks = json.load(f)
			except Exception as e:
				messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
				self.tasks = []
	def update_task_list(self):
		self.task_listbox.delete(0, tk.END)
		# Sort tasks by priority (High first) and completion status
		priority_order = {"High": 0, "Medium": 1, "Low": 2}
		self.tasks.sort(key=lambda x: (x["completed"], priority_order[x["priority"]]))
		for task in self.tasks:
			status = "✓" if task["completed"] else "○"
			display_text = f"{status} [{task['priority']}] {task['text']}"
			self.task_listbox.insert(tk.END, display_text)
			# Change color for completed tasks
			if task["completed"]:
				self.task_listbox.itemconfig(tk.END, {'fg': 'gray'})
	def add_task(self):
		task_text = self.task_entry.get().strip()
		priority = self.priority_var.get()
		if not task_text:
			messagebox.showwarning("Warning", "Please enter a task.")
			return
		task = {
			"text": task_text,
			"priority": priority,
			"completed": False
		}
		self.tasks.append(task)
		self.update_task_list()
		self.task_entry.delete(0, tk.END)
		self.status_var.set(f"Total tasks: {len(self.tasks)}")

	def mark_complete(self):
		selected_index = self.task_listbox.curselection()
		if not selected_index:
			messagebox.showwarning("Warning", "Please select a task to mark as complete.")
			return
		index = selected_index[0]
		self.tasks[index]["completed"] = not self.tasks[index]["completed"]
		self.update_task_list()

	def edit_task(self, event=None):
		selected_index = self.task_listbox.curselection()
		if not selected_index:
			messagebox.showwarning("Warning", "Please select a task to edit.")
			return
		index = selected_index[0]
		task = self.tasks[index]
		# Create dialog for editing
		new_text = simpledialog.askstring("Edit Task", "Edit task text:", 
										 initialvalue=task["text"])
		if new_text is None:  # User cancelled
			return
		new_text = new_text.strip()
		if not new_text:
			messagebox.showwarning("Warning", "Task cannot be empty.")
			return
		# Ask for priority if needed
		new_priority = simpledialog.askstring("Edit Priority", 
											 "Enter priority (Low, Medium, High):",
											 initialvalue=task["priority"])
		if new_priority is None:  # User cancelled
			return
		if new_priority not in ["Low", "Medium", "High"]:
			messagebox.showwarning("Warning", "Priority must be Low, Medium, or High.")
			return
		# Update task
		self.tasks[index]["text"] = new_text
		self.tasks[index]["priority"] = new_priority
		self.update_task_list()

	def delete_task(self):
		selected_index = self.task_listbox.curselection()
		if not selected_index:
			messagebox.showwarning("Warning", "Please select a task to delete.")
			return
		index = selected_index[0]
		confirm = messagebox.askyesno("Confirm Delete", 
									 f"Are you sure you want to delete '{self.tasks[index]['text']}'?")
		if confirm:
			del self.tasks[index]
			self.update_task_list()
			self.status_var.set(f"Total tasks: {len(self.tasks)}")
	def create_gui(self):
		# Main frame
		main_frame = ttk.Frame(self.root, padding="10")
		main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		# Configure grid weights
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		main_frame.columnconfigure(1, weight=1)
		main_frame.rowconfigure(1, weight=1)
		# Task entry
		ttk.Label(main_frame, text="New Task:").grid(row=0, column=0, sticky=tk.W, pady=5)
		self.task_entry = ttk.Entry(main_frame, width=40)
		self.task_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
		# Priority selection
		ttk.Label(main_frame, text="Priority:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
		self.priority_var = tk.StringVar()
		priority_combo = ttk.Combobox(main_frame, textvariable=self.priority_var, 
									 values=["Low", "Medium", "High"], state="readonly", width=10)
		priority_combo.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)
		priority_combo.set("Medium")
		# Add task button
		add_btn = ttk.Button(main_frame, text="Add Task", command=self.add_task)
		add_btn.grid(row=0, column=4, sticky=tk.W, pady=5, padx=5)
		# Task list frame
		list_frame = ttk.Frame(main_frame)
		list_frame.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
		list_frame.columnconfigure(0, weight=1)
		list_frame.rowconfigure(0, weight=1)
		# Task list with scrollbar
		self.task_listbox = tk.Listbox(list_frame, height=15, selectmode=tk.SINGLE)
		self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
		scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
		self.task_listbox.configure(yscrollcommand=scrollbar.set)
		# Bind double-click to edit task
		self.task_listbox.bind("<Double-Button-1>", self.edit_task)
		# Button frame
		button_frame = ttk.Frame(main_frame)
		button_frame.grid(row=2, column=0, columnspan=5, pady=10)
		# Action buttons
		complete_btn = ttk.Button(button_frame, text="Mark Complete", command=self.mark_complete)
		complete_btn.grid(row=0, column=0, padx=5)
		edit_btn = ttk.Button(button_frame, text="Edit Task", command=self.edit_task)
		edit_btn.grid(row=0, column=1, padx=5)
		delete_btn = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
		delete_btn.grid(row=0, column=2, padx=5)
		save_btn = ttk.Button(button_frame, text="Save Tasks", command=self.save_tasks)
		save_btn.grid(row=0, column=3, padx=5)
		# Status label
		self.status_var = tk.StringVar()
		self.status_var.set(f"Total tasks: {len(self.tasks)}")
		status_label = ttk.Label(main_frame, textvariable=self.status_var)
		status_label.grid(row=3, column=0, columnspan=5, pady=5)
	def __init__(self, root):
		self.root = root
		self.root.title("To-Do List Application")
		self.root.geometry("600x500")
		self.root.resizable(True, True)
		# Initialize tasks list
		self.tasks = []
		# Load tasks from file if exists
		self.load_tasks()
		# Create GUI
		self.create_gui()
		# Populate tasks list
		self.update_task_list()


# Step 8: Create the Main Function
def main():
	root = tk.Tk()
	app = TodoApp(root)
	root.mainloop()

if __name__ == "__main__":
	main()
