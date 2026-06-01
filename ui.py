import tkinter as tk 

class TodoListApp :
    def __init__(self, root) :
        self.root = root 
        self.root.title("To Do List App") 
        self.tasks = [] 
        self.create_widgets() 

    def create_widgets(self) :
        # Create an entry widget to input tasks 
        self.task_entry = tk.Entry(self.root, width=40) 
        self.task_entry.pack(pady=10) 

        # Create a button to add tasks 
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task) 
        self.add_button.pack(pady=5) 

        # Create a listbox to display tasks 
        self.task_listbox = tk.Listbox(self.root, width=50, height=10) 
        self.task_listbox.pack(pady=10) 

    def add_task(self) :
        task = self.task_entry.get() 
        if task : 
            self.tasks.append(task) 
            self.update_task_listbox() 
            self.task_entry.delete(0, tk.END) 

    def update_task_listbox(self) :
        self.task_listbox.delete(0, tk.END) 
        for task in self.tasks : 
            self.task_listbox.insert(tk.END, task)
            