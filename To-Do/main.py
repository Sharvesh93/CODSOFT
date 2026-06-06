import json
class TodoApp:
    def __init__(self):
        self.tasks = {}  # Dictionary to store tasks with unique IDs
        self.next_id = 1
    def priority(self, task):
        pass

    def add_task(self , task):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)
        self.tasks[self.next_id] = task
        self.next_id += 1
    
    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]

    def view_tasks(self):
        for task_id, task in self.tasks.items():
            print(f"Task ID: {task_id}, Description: {task}")
    
    def run(self) : 
        while True:
            print("\nTo-Do List Application")
            print("1. View Tasks")
            print("2. Add Task")
            print("3. Change Priority")
            print("4. Update Task")
            print("5. Delete Task")
            print("6. Exit")
            choice = input("Enter your choice: ")
            
            # View tasks 
            if choice == '1':
                self.view_tasks()
            
            # Add task 
            elif choice == '2':
                task_desc = input("Enter task description: ")
                self.add_task(task_desc)
                
                print("Task added successfully.")
            
            # Change priority 
            elif choice == '3':
                try:
                    task_id = int(input("Enter task ID to change priority: "))
                    new_priority = input("Enter new priority (High/Medium/Low): ")
                    self.priority(task_id, new_priority)
                    
                    print("Priority changed successfully.")
                except ValueError:
                    print("Invalid input. Please enter a valid task ID.")
            
            # Delete task
            elif choice == '4':
                try:
                    task_id = int(input("Enter task ID to delete: "))
                    self.delete_task(task_id)
                    
                    print("Task deleted successfully.")
                except ValueError:
                    print("Invalid input. Please enter a valid task ID.")
            
            # Update task 
            elif choice == '5':
                pass 
                # To implement the update the task state either done or not done

            # Exit application
            elif choice == '6':
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = TodoApp()
    app.run()

"""

JSON file format will be : 
1) description : string
2) priority : string (High/Medium/Low)
3) status : string (Done/Not yet)

"""